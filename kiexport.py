
#=============================================================================================#

# KiExport
# Tool to export manufacturing files from KiCad PCB projects.
# Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)
# Version: 0.0.7
# Last Modified: +05:30 22:18:24 PM 30-08-2024, Friday
# GitHub: https://github.com/vishnumaiea/KiExport
# License: MIT

#=============================================================================================#

import subprocess
import argparse
import os
import re
from datetime import datetime
import zipfile

#=============================================================================================#

SAMPLE_PCB_FILE = "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"

#=============================================================================================#

def generateGerbers (output_dir, pcb_filename, to_overwrite = True):
  # Common base command
  gerber_export_command = ["kicad-cli", "pcb", "export", "gerbers"]

  # Assemble the full command for Gerber export
  # output_dir = "Mitayi-Pico-D1/Gerber"
  layer_list = "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,User.Drawings,User.Comments,Edge.Cuts,F.Courtyard,B.Courtyard,F.Fab,B.Fab"
  # pcb_filename = "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"

  if not check_file_exists (pcb_filename):
    print (f"generateGerbers [ERROR]: {pcb_filename} does not exist.")
    return

  file_name = extract_pcb_file_name (pcb_filename)
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  
  print (f"generateGerbers [INFO]: Project name is {project_name} and revision is {info ['rev']}.")
  
  # Check if the ouptut directory exists, and create if not.
  if not os.path.exists (output_dir):
    print (f"generateGerbers [INFO]: Output directory {output_dir} does not exist. Creating it now.")
    os.makedirs (output_dir)

  rev_directory = f"{output_dir}/R{info ['rev']}"

  if not os.path.exists (rev_directory):
    print (f"generateGerbers [INFO]: Revision directory {rev_directory} does not exist. Creating it now.")
    os.makedirs (rev_directory)
  
  not_completed = True
  seq_number = 0
  
  while not_completed:
    today_date = datetime.now()
    formatted_date = today_date.strftime ("%d-%m-%Y")
    filename_date = today_date.strftime ("%d%m%Y")
    seq_number += 1
    date_directory = f"{rev_directory}/[{seq_number}] {formatted_date}"
    target_directory = f"{date_directory}/Gerber"

    if not os.path.exists (target_directory):
      print (f"generateGerbers [INFO]: Target directory {target_directory} does not exist. Creating it now.")
      os.makedirs (target_directory)
      generateDrills (target_directory, pcb_filename)
      not_completed = False
    else:
      if to_overwrite:
        print (f"generateGerbers [INFO]: Target directory {target_directory} already exists. Any files will be overwritten.")
        delete_non_zip_files (target_directory)
        generateDrills (target_directory, pcb_filename)
        not_completed = False
      else:
        print (f"generateGerbers [INFO]: Target directory {target_directory} already exists. Creating another one.")
        not_completed = True

  full_command = gerber_export_command + \
                ["--output", target_directory] + \
                ["--no-protel-ext"] + \
                ["--layers", layer_list] + \
                ["--no-netlist"] + \
                ["--use-drill-file-origin"] + \
                [pcb_filename]
  
  # Run the command
  try:
    subprocess.run (full_command, check = True)
    print ("generateGerbers [OK]: Gerber files exported successfully.")

    # Rename the files by adding Revision after the project name
    for filename in os.listdir (target_directory):
      if filename.startswith (project_name) and not filename.endswith ('.zip'):
        # Construct the new filename with the revision tag
        base_name = filename [len (project_name):]  # Remove the project name part
        new_filename = f"{project_name}-R{info ['rev']}{base_name}"
        
        # Full paths for renaming
        old_file_path = os.path.join (target_directory, filename)
        new_file_path = os.path.join (target_directory, new_filename)
        
        # Rename the file
        os.rename (old_file_path, new_file_path)
        # print(f"Renamed: {filename} -> {new_filename}")
    
    seq_number = 1
    not_completed = True
    
    while not_completed:
      zip_file_name = f"{project_name}-R{info ['rev']}-Gerber-{filename_date}-{seq_number}.zip"

      if os.path.exists (f"{target_directory}/{zip_file_name}"):
        seq_number += 1
      else:
        zip_all_files (target_directory, f"{target_directory}/{zip_file_name}")
        print (f"generateGerbers [OK]: ZIP file {zip_file_name} created successfully.")
        not_completed = False

  except subprocess.CalledProcessError as e:
    print (f"generateGerbers [ERROR]: Error occurred: {e}")

#=============================================================================================#

def delete_non_zip_files (directory):
  """
  Deletes all files in the specified directory except ZIP files.

  Args:
    directory (str): Path to the directory where the cleanup will occur.
  """
  for filename in os.listdir (directory):
    file_path = os.path.join (directory, filename)
    if os.path.isfile (file_path) and not filename.endswith ('.zip'):
      os.remove (file_path)
      # print(f"Deleted: {filename}")
      
#=============================================================================================#

def generateDrills (target_dir, pcb_filename):
  # Common base command
  drill_export_command = ["kicad-cli", "pcb", "export", "drill"]

  file_name = extract_pcb_file_name (pcb_filename)
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)

  # Check if the target directory ends with a slash, and add one if not
  if target_dir[-1] != '/':
    target_dir += '/'
  
  full_command = drill_export_command + \
                ["--output", target_dir] + \
                ["--format", "excellon"] + \
                ["--drill-origin", "plot"] + \
                ["--excellon-zeros-format", "decimal"] + \
                ["--excellon-oval-format", "route"] + \
                ["--excellon-units", "mm"] + \
                ["--excellon-separate-th"] + \
                ["--generate-map"] + \
                ["--map-format", "pdf"] + \
                [pcb_filename]
  
  # Run the command
  try:
    subprocess.run (full_command, check = True)
    print ("generateDrills [OK]: Drill files exported successfully.")

    # Rename the files by adding Revision after the project name
    for filename in os.listdir (target_dir):
      if filename.startswith (project_name) and not filename.endswith ('.zip'):
        # Construct the new filename with the revision tag
        base_name = filename [len (project_name):]  # Remove the project name part
        new_filename = f"{project_name}-R{info ['rev']}{base_name}"
        
        # Full paths for renaming
        old_file_path = os.path.join (target_dir, filename)
        new_file_path = os.path.join (target_dir, new_filename)
        
        # Rename the file
        os.rename (old_file_path, new_file_path)
        # print(f"Renamed: {filename} -> {new_filename}")
        
  except subprocess.CalledProcessError as e:
    print (f"generateDrills [ERROR]: Error occurred: {e}")

#=============================================================================================#

def zip_all_files (source_folder, zip_file_path):
  """
  Compresses all files from a folder into a ZIP file.

  Args:
      source_folder (str): Path to the folder containing files.
      zip_file_path (str): Path where the ZIP file will be saved.
  """
  with zipfile.ZipFile (zip_file_path, 'w') as zipf:
    for foldername, subfolders, filenames in os.walk (source_folder):
      for filename in filenames:
        file_path = os.path.join (foldername, filename)
        # Exclude the ZIP file itself from being added
        if os.path.abspath (file_path) != os.path.abspath (zip_file_path) and not filename.endswith('.zip'):
          zipf.write (file_path, arcname = os.path.relpath (file_path, source_folder))
    
    # print (f"ZIP file created: {os.path.basename (zip_file_path)}")

#=============================================================================================#

def check_file_exists (file_name):
  """
  Checks if the input PCB file exists.
  Args:
    input_file_name (str): The path to the PCB file.
  Returns:
    bool: True if the file exists, False otherwise.
  """
  return os.path.exists (file_name)

#=============================================================================================#

def extract_project_name (file_name):
  """
  Extracts the project name from a given PCB file name by removing the extension.
  Args:
    input_file_name (str): The PCB file name.
  Returns:
    str: The project name without the file extension.
  """
  file_name = extract_pcb_file_name (file_name)
  project_name = os.path.splitext (file_name) [0]
  # print ("Project name is ", project_name)

  return project_name

#=============================================================================================#

def extract_pcb_file_name (file_name):
  """
  Extracts the PCB file name from a given path.
  Args:
    input_file_name (str): The path to the PCB file.
  Returns:
    str: The PCB file name without any directory path.
  """
  return os.path.basename (file_name)

#=============================================================================================#

def extract_info_from_pcb (pcb_file_path):
  """
  Extracts specific information from a KiCad PCB file.
  Args:
    pcb_file_path (str): Path to the KiCad PCB file.
  Returns:
    dict: A dictionary containing the extracted information.
  """
  info = {}
  
  try:
    with open (pcb_file_path, 'r') as file:
      content = file.read()
    
    # Regular expressions to extract information
    title_match = re.search (r'\(title "([^"]+)"\)', content)
    date_match = re.search (r'\(date "([^"]+)"\)', content)
    rev_match = re.search (r'\(rev "([^"]+)"\)', content)
    company_match = re.search (r'\(company "([^"]+)"\)', content)
    comment1_match = re.search (r'\(comment 1 "([^"]+)"\)', content)
    comment2_match = re.search (r'\(comment 2 "([^"]+)"\)', content)
    
    # Store matches in the dictionary
    if title_match:
      info ['title'] = title_match.group (1)
    if date_match:
      info ['date'] = date_match.group (1)
    if rev_match:
      info ['rev'] = rev_match.group (1)
    if company_match:
      info ['company'] = company_match.group (1)
    if comment1_match:
      info ['comment1'] = comment1_match.group (1)
    if comment2_match:
      info ['comment2'] = comment2_match.group (1)
      
  except FileNotFoundError:
    print (f"Error: The file '{pcb_file_path}' does not exist.")
  except Exception as e:
    print (f"Error occurred: {e}")
  
  return info

#=============================================================================================#

def test():
  info = extract_info_from_pcb (SAMPLE_PCB_FILE)
  print (info)
  print (f"Revision is {info ['rev']}")

#=============================================================================================#

def parseArguments():
  parser = argparse.ArgumentParser (description = "KiExport: Tool to export manufacturing files from KiCad PCB projects.")
  subparsers = parser.add_subparsers (dest = "command", help = "Available commands.")

  # Subparser for the Gerber export command
  gerber_parser = subparsers.add_parser ("gerbers", help = "Export Gerber files.")
  gerber_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  gerber_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Gerber files to.")

  test_parser = subparsers.add_parser ("test", help = "Test.")

  # Parse arguments
  args = parser.parse_args()

  if args.command == "gerbers":    
    # Call the generateGerbers function with the parsed arguments
    generateGerbers (args.output_dir, args.input_filename)

  elif args.command == "test":
    test()
    
  else:
    parser.print_help()

#=============================================================================================#

def main():
  parseArguments()

#=============================================================================================#

if __name__ == "__main__":
  main()

#=============================================================================================#
