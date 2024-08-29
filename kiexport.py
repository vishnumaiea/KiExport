
#=============================================================================================#

# KiExport
# Tool to export manufacturing files from KiCad PCB projects.
# Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)
# Version: 0.0.4
# Last Modified: +05:30 23:40:47 PM 29-08-2024, Thursday
# GitHub: https://github.com/vishnumaiea/KiExport
# License: MIT

#=============================================================================================#

import subprocess
import argparse
import os

#=============================================================================================#

def generateGerbers (output_dir, pcb_filename):
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
  print (f"generateGerbers [INFO]: Project name is {project_name}.")
  
  # Check if the ouptut directory exists, and create if not.
  if not os.path.exists (output_dir):
    print (f"generateGerbers [INFO]: Output directory {output_dir} does not exist. Creating it now.")
    os.makedirs (output_dir)

  full_command = gerber_export_command + \
                ["--output", output_dir] + \
                ["--no-protel-ext"] + \
                ["--layers", layer_list] + \
                ["--no-netlist"] + \
                ["--use-drill-file-origin"] + \
                [pcb_filename]
  
  # Run the command
  try:
    subprocess.run (full_command, check = True)
    print ("generateGerbers [OK]: Gerber files exported successfully.")
  except subprocess.CalledProcessError as e:
    print (f"generateGerbers [ERROR]: Error occurred: {e}")

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

def parseArguments():
  parser = argparse.ArgumentParser (description = "KiExport: Tool to export manufacturing files from KiCad PCB projects.")
  subparsers = parser.add_subparsers (dest = "command", help = "Available commands.")

  # Subparser for the Gerber export command
  gerber_parser = subparsers.add_parser ("gerbers", help = "Export Gerber files.")
  gerber_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  gerber_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Gerber files to.")

  # Parse arguments
  args = parser.parse_args()

  if args.command == "gerbers":    
    # Call the generateGerbers function with the parsed arguments
    generateGerbers (args.output_dir, args.input_filename)
  else:
    parser.print_help()

#=============================================================================================#

def main():
  parseArguments()

#=============================================================================================#

if __name__ == "__main__":
  main()

#=============================================================================================#
