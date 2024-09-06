
#=============================================================================================#

# KiExport
# Tool to export manufacturing files from KiCad PCB projects.
# Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)
# Version: 0.0.14
# Last Modified: +05:30 00:01:31 AM 07-09-2024, Saturday
# GitHub: https://github.com/vishnumaiea/KiExport
# License: MIT

#=============================================================================================#

import subprocess
import argparse
import os
import re
from datetime import datetime
import zipfile
import json

#=============================================================================================#

APP_NAME = "KiExport"
APP_VERSION = "0.0.14"

SAMPLE_PCB_FILE = "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"

current_config = None
default_config = None
DEFAULT_CONFIG_JSON = '''
{
  "name": "KiExport.JSON",
  "description": "Configuration file for KiExport",
  "filetype": "json",
  "version": "1.0",
  "commands": ["gerbers", "drills", "sch_pdf", "bom", "pcb_pdf", "positions", "ddd"],
  "data": {
    "gerbers": {
      "--output_dir": "",
      "--layers": ["F.Cu","B.Cu","F.Paste","B.Paste","F.Silkscreen","B.Silkscreen","F.Mask","B.Mask","User.Drawings","User.Comments","Edge.Cuts","F.Courtyard","B.Courtyard","F.Fab","B.Fab"],
      "--drawing-sheet": false,
      "--exclude-refdes": false,
      "--exclude-value": false,
      "--include-border-title": false,
      "--no-x2": false,
      "--no-netlist": true,
      "--subtract-soldermask": false,
      "--disable-aperture-macros": false,
      "--use-drill-file-origin": true,
      "--precision": 6,
      "--no-protel-ext": true,
      "--common-layers": false,
      "--board-plot-params": false,
      "kie_include_drill": true
    },
    "drills": {
      "--output_dir": "",
      "--format": "excellon",
      "--drill-origin": "plot",
      "--excellon-zeros-format": "decimal",
      "--excellon-oval-format": "route",
      "--excellon-units": "mm",
      "--excellon-mirror-y": false,
      "--excellon-min-header": false,
      "--excellon-separate-th": true,
      "--generate-map": true,
      "--map-format": "pdf",
      "--gerber-precision": false
    },
    "bom": {
      "CSV": {
        "--output_dir": "",
        "--preset": "Group by MPN-DNP",
        "--format-preset": "CSV",
        "--fields": "${ITEM_NUMBER},Reference,Value,Name,Footprint,${QUANTITY},${DNP},MPN,MFR,Alt MPN",
        "--labels": "#,Reference,Value,Name,Footprint,Qty,DNP,MPN,MFR,Alt MPN",
        "--group-by": "${DNP},MPN",
        "--sort-field": false,
        "--sort-asc": false,
        "--filter": false,
        "--exclude-dnp": false,
        "--field-delimiter": false,
        "--string-delimiter": false,
        "--ref-delimiter": false,
        "--ref-range-delimiter": false,
        "--keep-tabs": false,
        "--keep-line-breaks": false
      }
    },
    "sch_pdf": {
      "--output_dir": "",
      "--drawing-sheet": false,
      "--theme": "User",
      "--black-and-white": false,
      "--exclude-drawing-sheet": false,
      "--exclude-pdf-property-popups": false,
      "--no-background-color": false,
      "--pages": false
    },
    "pcb_pdf": {
      "--output_dir": "",
      "--layers": ["F.Cu","B.Cu","F.Paste","B.Paste","F.Silkscreen","B.Silkscreen","F.Mask","B.Mask","User.Drawings","User.Comments","Edge.Cuts","F.Courtyard","B.Courtyard","F.Fab","B.Fab"],
      "--drawing-sheet": false,
      "--mirror": false,
      "--exclude-refdes": false,
      "--exclude-value": false,
      "--include-border-title": true,
      "--negative": false,
      "--black-and-white": false,
      "--theme": "User",
      "--drill-shape-opt": 1,
      "kie_single_file": false
    },
    "positions": {
      "--output_dir": "",
      "--side": "front,back,both",
      "--format": "csv",
      "--units": "mm",
      "--bottom-negate-x": false,
      "--use-drill-file-origin": true,
      "--smd-only": false,
      "--exclude-fp-th": false,
      "--exclude-dnp": false,
      "--gerber-board-edge": false
    },
    "ddd": {
      "STEP": {
        "--output_dir": "",
        "--force": true,
        "--grid-origin": false,
        "--drill-origin": false,
        "--no-unspecified": false,
        "--no-dnp": false,
        "--subst-models": true,
        "--board-only": false,
        "--include-tracks": true,
        "--include-zones": true,
        "--min-distance": false,
        "--no-optimize-step": false,
        "--user-origin": false
      },
      "VRML": {
        "--output_dir": "",
        "--force": true,
        "--user-origin": false,
        "--units": "mm",
        "--models-dir": false,
        "--models-relative": false
      }
    }
  }
}
'''

#=============================================================================================#

class Colorize:
    def __init__(self, text):
        self.text = text
        self.ansi_code = '\033[0m'  # Default to reset

    def _color_text (self):
        return f"{self.ansi_code}{self.text}\033[0m"

    def red (self):
        self.ansi_code = '\033[31m'
        return self._color_text()

    def green (self):
        self.ansi_code = '\033[32m'
        return self._color_text()

    def yellow (self):
        self.ansi_code = '\033[33m'
        return self._color_text()

    def blue (self):
        self.ansi_code = '\033[34m'
        return self._color_text()

    def magenta (self):
        self.ansi_code = '\033[35m'
        return self._color_text()

    def cyan (self):
        self.ansi_code = '\033[36m'
        return self._color_text()

# Define ANSI escape codes for colors
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'reset': '\033[0m'
}

class _color:
    def __call__(self, text, color):
        return f"{COLORS[color]}{text}{COLORS['reset']}"
    
    def __getattr__(self, color):
        if color in COLORS:
            return lambda text: self(text, color)
        raise AttributeError(f"Color '{color}' is not supported.")

# Create an instance of the Colorize class
color = _color()

#=============================================================================================#

def generateGerbers (output_dir, pcb_filename, to_overwrite = True):
  # Common base command
  gerber_export_command = ["kicad-cli", "pcb", "export", "gerbers"]

  # Check if the pcb file exists
  if not check_file_exists (pcb_filename):
    print (color.red (f"generateGerbers [ERROR]: '{pcb_filename}' does not exist."))
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (pcb_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen
  
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  print (f"generateGerbers [INFO]: Project name is '{color.magenta (project_name)}' and revision is {info ['rev']}.")
  
  #---------------------------------------------------------------------------------------------#
  
  # Read the target directory name from the config file
  config_dir = current_config.get ("data", {}).get ("gerbers", {}).get ("--output_dir", default_config ["data"]["gerbers"]["--output_dir"])
  command_dir = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (config_dir, command_dir, "Gerber", info ["rev"], "generateGerbers")

  #---------------------------------------------------------------------------------------------#
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("gerbers", {})

  seq_number = 1
  not_completed = True
  full_command = []
  full_command.extend (gerber_export_command) # Add the base command
  full_command.append ("--output")
  full_command.append (f'"{final_directory}"')
  
  # Add the remaining arguments.
  # Check if the argument list is not an empty dictionary.
  if arg_list:
    for key, value in arg_list.items():
      if key.startswith ("--"): # Only fetch the arguments that start with "--"
        if key == "--output_dir": # Skip the --output_dir argument, sice we already added it
          continue
        elif key == "--layers":
          full_command.append (key)
          layers_csv = ",".join (value) # Convert the list to a comma-separated string
          full_command.append (f'"{layers_csv}"')
        else:
          # Check if the value is empty
          if value == "": # Skip if the value is empty
            continue
          else:
            # Check if the vlaue is a JSON boolean
            if isinstance (value, bool):
              if value == True: # If the value is true, then append the key as an argument
                full_command.append (key)
            else:
              # Check if the value is a string and not a numeral
              if isinstance (value, str) and not value.isdigit():
                  full_command.append (key)
                  full_command.append (f'"{value}"') # Add as a double-quoted string
              elif isinstance (value, (int, float)):
                  full_command.append (key)
                  full_command.append (str (value))  # Append the numeric value as string
  
  # Finally add the input file
  full_command.append (f'"{pcb_filename}"')
  print ("generateGerbers [INFO]: Running command: ", color.blue (' '.join (full_command)))
  
  #---------------------------------------------------------------------------------------------#
  
  # Delete the existing files in the output directory
  delete_files (final_directory, include_extensions = [".gbr", ".gbrjob"])
  
  #---------------------------------------------------------------------------------------------#
  
  # Run the command
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
    print (color.green ("generateGerbers [OK]: Gerber files exported successfully."))
  
  except subprocess.CalledProcessError as e:
    print (color.red (f"generateGerbers [ERROR]: Error occurred: {e}"))
    return
  
  #---------------------------------------------------------------------------------------------#
  
  # Rename the files by adding Revision after the project name.
  rename_files (final_directory, project_name, info ['rev'], [".gbr", ".gbrjob"])
  
  #---------------------------------------------------------------------------------------------#
  
  seq_number = 1
  not_completed = True
  
  # Sequentially name and create the zip files.
  while not_completed:
    zip_file_name = f"{project_name}-R{info ['rev']}-Gerber-{filename_date}-{seq_number}.zip"

    if os.path.exists (f"{final_directory}/{zip_file_name}"):
      seq_number += 1
    else:
      # zip_all_files (final_directory, f"{final_directory}/{zip_file_name}")
      zip_all_files_2 (final_directory, [".gbr", ".gbrjob"], zip_file_name)
      print (f"generateGerbers [OK]: ZIP file '{color.magenta (zip_file_name)}' created successfully.")
      print()
      not_completed = False

#=============================================================================================#

def generateDrills (output_dir, pcb_filename):
  # Common base command
  drill_export_command = ["kicad-cli", "pcb", "export", "drill"]

  # Check if the pcb file exists
  if not check_file_exists (pcb_filename):
    print (color.red (f"generateDrills [ERROR]: '{pcb_filename}' does not exist."))
    return

  #-------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (pcb_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen
  
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  print (f"generateDrills [INFO]: Project name is '{color.magenta (project_name)}' and revision is {info ['rev']}.")
  
  #-------------------------------------------------------------------------------------------#

  # Read the target directory name from the config file
  config_dir = current_config.get ("data", {}).get ("drills", {}).get ("--output_dir", default_config ["data"]["drills"]["--output_dir"])
  command_dir = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (config_dir, command_dir, "Gerber", info ["rev"], "generateDrills")

  # Check if the final directory ends with a slash, and add one if not.
  if final_directory[-1] != "/":
    final_directory = f"{final_directory}/"
    
  #-------------------------------------------------------------------------------------------#
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("drills", {})

  seq_number = 1
  not_completed = True
  full_command = []
  full_command.extend (drill_export_command) # Add the base command
  full_command.append ("--output")
  full_command.append (f'"{final_directory}"')
  
  # Add the remaining arguments.
  # Check if the argument list is not an empty dictionary.
  if arg_list:
    for key, value in arg_list.items():
      if key.startswith ("--"): # Only fetch the arguments that start with "--"
        if key == "--output_dir": # Skip the --output_dir argument, sice we already added it
          continue
        else:
          # Check if the value is empty
          if value == "": # Skip if the value is empty
            continue
          else:
            # Check if the vlaue is a JSON boolean
            if isinstance (value, bool):
              if value == True: # If the value is true, then append the key as an argument
                full_command.append (key)
            else:
              # Check if the value is a string and not a numeral
              if isinstance (value, str) and not value.isdigit():
                  full_command.append (key)
                  full_command.append (f'"{value}"') # Add as a double-quoted string
              elif isinstance (value, (int, float)):
                  full_command.append (key)
                  full_command.append (str (value))  # Append the numeric value as string
  
  # Finally add the input file
  full_command.append (f'"{pcb_filename}"')
  print ("generateDrills [INFO]: Running command: ", color.blue (' '.join (full_command)))
  
  #-------------------------------------------------------------------------------------------#

  # Delete the existing files in the output directory
  delete_files (final_directory, include_extensions = [".drl", ".ps", ".pdf"])

  #-------------------------------------------------------------------------------------------#
  
  # Run the command
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
    print (color.green ("generateDrills [OK]: Drill files exported successfully."))
    print()
  
  except subprocess.CalledProcessError as e:
    print (color.red (f"generateDrills [ERROR]: Error occurred: {e}"))
    print()
    return
  
  #-------------------------------------------------------------------------------------------#

  # Rename the files by adding Revision after the project name.
  rename_files (final_directory, project_name, info ['rev'], [".drl", ".ps", ".pdf"])

#=============================================================================================#

def generatePositions (output_dir, pcb_filename, to_overwrite = True):
  global current_config  # Access the global config
  global default_config  # Access the global config
  
  # Common base command
  position_export_command = ["kicad-cli", "pcb", "export", "pos"]

  # Check if the input file exists
  if not check_file_exists (pcb_filename):
    print (f"generatePositions [ERROR]: {pcb_filename} does not exist.")
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (pcb_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen
  
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  print (f"generatePositions [INFO]: Project name is {project_name} and revision is {info ['rev']}.")
  
  #---------------------------------------------------------------------------------------------#

  # Read the target directory name from the config file
  config_dir = current_config.get ("data", {}).get ("positions", {}).get ("--output_dir", default_config ["data"]["positions"]["--output_dir"])
  command_dir = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (config_dir, command_dir, "Assembly", info ["rev"], "generatePositions")
  
  #---------------------------------------------------------------------------------------------#
  
  pos_front_filename = f"{final_directory}/{project_name}-Pos-Front.csv"
  pos_back_filename = f"{final_directory}/{project_name}-Pos-Back.csv"
  pos_all_filename = f"{final_directory}/{project_name}-Pos-All.csv"

  # Create a list of filenames for front, back, and both.
  pos_filenames = [pos_front_filename, pos_back_filename, pos_all_filename]

  # Create a list of three command sets for front, back, and both.
  full_command_list = []
  for filename in pos_filenames:
      full_command = position_export_command.copy()  # Copy the base command
      full_command.append ("--output")
      full_command.append (f'"{filename}"')
      full_command_list.append (full_command)
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("positions", {})
  sides = arg_list.get ("--side", None) # Get the sides from the config file as a string

  # Check if the sides are valid and apply the default value if not
  if sides == None or sides == "":
    print (f"generatePositions [INFO]: No sides specified. Using both sides.")
    sides = "both"
  
  # Add the remaining arguments.
  # Check if the argument list is not an empty dictionary.
  if arg_list:
    for i, command_set in enumerate (full_command_list):
      for key, value in arg_list.items():
        if key.startswith ("--"): # Only fetch the arguments that start with "--"
          if key == "--output_dir": # Skip the --output_dir argument, sice we already added it
            continue
          elif key == "--side":
            if sides.__contains__ ("front") and i == 0:
              command_set.append (key)
              command_set.append ("front")
            elif sides.__contains__ ("back") and i == 1:
              command_set.append (key)
              command_set.append ("back")
            elif sides.__contains__ ("both") and i == 2:
              command_set.append (key)
              command_set.append ("both")
          else:
            # Check if the value is empty
            if value == "": # Skip if the value is empty
              continue
            else:
              # Check if the vlaue is a JSON boolean
              if isinstance (value, bool):
                if value == True: # If the value is true, then append the key as an argument
                  command_set.append (key)
              else:
                # Check if the value is a string and not a numeral
                if isinstance (value, str) and not value.isdigit():
                    command_set.append (key)
                    command_set.append (f'"{value}"') # Add as a double-quoted string
                elif isinstance (value, (int, float)):
                    command_set.append (key)
                    command_set.append (str (value))  # Append the numeric value as string

  # Finally append the filename to the commands
  for command_set in full_command_list:
    # board_file_path = os.path.abspath (pcb_filename)
    command_set.append (f'"{pcb_filename}"')
  
  #---------------------------------------------------------------------------------------------#
  
  # Delete all non-zip files
  delete_non_zip_files (final_directory)
  
  #---------------------------------------------------------------------------------------------#
  
  # Run the commands
  for i, full_command in enumerate (full_command_list):
    if (sides.__contains__ ("front") and i == 0) or (sides.__contains__ ("back") and i == 1) or (sides.__contains__ ("both") and i == 2):
      try:
        command_string = ' '.join (full_command)  # Convert the list to a string
        print (f"generatePositions [INFO]: Running command: {command_string}")
        subprocess.run (command_string, check = True)
      except subprocess.CalledProcessError as e:
        print (f"generatePositions [ERROR]: Error occurred while generating the files.")
        return

  print ("generatePositions [OK]: Position files exported successfully.")
  
  #---------------------------------------------------------------------------------------------#
  
  # Rename the files by adding Revision after the project name.
  for filename in os.listdir (final_directory):
    if filename.startswith (project_name) and not filename.endswith ('.zip'):
      # Construct the new filename with the revision tag
      base_name = filename [len (project_name):]  # Remove the project name part
      new_filename = f"{project_name}-R{info ['rev']}{base_name}"
      
      # Full paths for renaming
      old_file_path = os.path.join (final_directory, filename)
      new_file_path = os.path.join (final_directory, new_filename)
      
      # Rename the file
      os.rename (old_file_path, new_file_path)
      # print(f"Renamed: {filename} -> {new_filename}")
  
  #---------------------------------------------------------------------------------------------#
  
  seq_number = 1
  not_completed = True
  
  # Sequentially name and create the zip files.
  while not_completed:
    zip_file_name = f"{project_name}-R{info ['rev']}-Position-Files-{filename_date}-{seq_number}.zip"

    if os.path.exists (f"{final_directory}/{zip_file_name}"):
      seq_number += 1
    else:
      zip_all_files (final_directory, f"{final_directory}/{zip_file_name}")
      print (f"generatePositions [OK]: ZIP file {zip_file_name} created successfully.")
      not_completed = False

#=============================================================================================#

def generatePcbPdf (output_dir, pcb_filename, to_overwrite = True):
  # Common base command
  pcb_pdf_export_command = ["kicad-cli", "pcb", "export", "pdf"]

  layer_list = "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,User.Drawings,User.Comments,Edge.Cuts,F.Courtyard,B.Courtyard,F.Fab,B.Fab"

  if not check_file_exists (pcb_filename):
    print (f"generatePcbPdf [ERROR]: {pcb_filename} does not exist.")
    return

  file_name = extract_pcb_file_name (pcb_filename)
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  
  print (f"generatePcbPdf [INFO]: Project name is {project_name} and revision is {info ['rev']}.")
  
  # Check if the ouptut directory exists, and create if not.
  if not os.path.exists (output_dir):
    print (f"generatePcbPdf [INFO]: Output directory {output_dir} does not exist. Creating it now.")
    os.makedirs (output_dir)

  rev_directory = f"{output_dir}/R{info ['rev']}"

  if not os.path.exists (rev_directory):
    print (f"generatePcbPdf [INFO]: Revision directory {rev_directory} does not exist. Creating it now.")
    os.makedirs (rev_directory)
  
  not_completed = True
  seq_number = 0
  
  while not_completed:
    today_date = datetime.now()
    formatted_date = today_date.strftime ("%d-%m-%Y")
    filename_date = today_date.strftime ("%d%m%Y")
    seq_number += 1
    date_directory = f"{rev_directory}/[{seq_number}] {formatted_date}"
    target_directory = f"{date_directory}/PCB"

    if not os.path.exists (target_directory):
      print (f"generatePcbPdf [INFO]: Target directory {target_directory} does not exist. Creating it now.")
      os.makedirs (target_directory)
      not_completed = False
    else:
      if to_overwrite:
        print (f"generatePcbPdf [INFO]: Target directory {target_directory} already exists. Any files will be overwritten.")
        delete_non_zip_files (target_directory)
        not_completed = False
      else:
        print (f"generatePcbPdf [INFO]: Target directory {target_directory} already exists. Creating another one.")
        not_completed = True

  # # Check if the target directory ends with a slash, and add one if not
  # if target_directory [-1] != '/':
  #   target_directory += '/'
  
  for layer_name in layer_list.split (","):
    full_command_1 = pcb_pdf_export_command + \
                  ["--output", f"{target_directory}/{project_name}-{layer_name}.pdf"] + \
                  ["--layers", f"{layer_name},Edge.Cuts"] + \
                  ["--include-border-title"] + \
                  ["--theme", "User"] + \
                  ["--drill-shape-opt", "1"] + \
                  [pcb_filename]
    # Run the command
    try:
      subprocess.run (full_command_1, check = True)
    
    except subprocess.CalledProcessError as e:
      print (f"generatePcbPdf [ERROR]: Error occurred: {e}")
      return

  print ("generatePcbPdf [OK]: PCB PDF files exported successfully.")
    
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
    
    # seq_number = 1
    # not_completed = True
    
    # while not_completed:
    #   zip_file_name = f"{project_name}-R{info ['rev']}-PCB-PDF-{filename_date}-{seq_number}.zip"

    #   if os.path.exists (f"{target_directory}/{zip_file_name}"):
    #     seq_number += 1
    #   else:
    #     zip_all_files (target_directory, f"{target_directory}/{zip_file_name}")
    #     print (f"generatePcbPdf [OK]: ZIP file {zip_file_name} created successfully.")
    #     not_completed = False

#=============================================================================================#

def generateSchPdf (output_dir, sch_filename, to_overwrite = True):
  global current_config  # Access the global config
  global default_config  # Access the global config

  # Common base command
  sch_pdf_export_command = ["kicad-cli", "sch", "export", "pdf"]

  # Check if the input file exists
  if not check_file_exists (sch_filename):
    print (f"generateSchPdf [ERROR]: '{sch_filename}' does not exist.")
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (sch_filename) # Extract information from the input file
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen

  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (sch_filename) # Extract basic information from the input file
  print (f"generateSchPdf [INFO]: Project name is '{project_name}' and revision is R{info ['rev']}.")

  #---------------------------------------------------------------------------------------------#

  # Read the target directory name from the config file
  config_dir = current_config.get ("data", {}).get ("sch_pdf", {}).get ("--output_dir", default_config ["data"]["sch_pdf"]["--output_dir"])
  command_dir = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (config_dir, command_dir, "SCH", info ["rev"], "generateSchPdf")
  
  #---------------------------------------------------------------------------------------------#
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("sch_pdf", {})

  seq_number = 1
  not_completed = True
  full_command = []
  full_command.extend (sch_pdf_export_command) # Add the base command
  
  # Create the output file name.
  while not_completed:
    file_name = f"{final_directory}/{project_name}-R{info ['rev']}-SCH-{filename_date}-{seq_number}.pdf"

    if os.path.exists (file_name):
      seq_number += 1 # Increment the sequence number and try again
      not_completed = True
    else:
      full_command.append ("--output")
      full_command.append (f'"{file_name}"') # Add the output file name with double quotes around it
      break
  
  # Add the remaining arguments.
  # Check if the argument list is not an empty dictionary.
  if arg_list:
    for key, value in arg_list.items():
      if key.startswith ("--"): # Only fetch the arguments that start with "--"
        if key == "--output_dir": # Skip the --output_dir argument, sice we already added it
          continue
        else:
          # Check if the value is empty
          if value == "": # Skip if the value is empty
            continue
          else:
            # Check if the vlaue is a JSON boolean
            if isinstance (value, bool):
              if value == True: # If the value is true, then append the key as an argument
                full_command.append (key)
            else:
              # Check if the value is a string and not a numeral
              if isinstance (value, str) and not value.isdigit():
                  full_command.append (key)
                  full_command.append (f'"{value}"') # Add as a double-quoted string
              elif isinstance (value, (int, float)):
                  full_command.append (key)
                  full_command.append (str (value))  # Append the numeric value as string
  
  # Finally add the input file
  full_command.append (f'"{sch_filename}"')
  print ("generateSchPdf [INFO]: Running command: ", full_command)

  #---------------------------------------------------------------------------------------------#
  
  # Run the command
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
  
  except subprocess.CalledProcessError as e:
    print (f"generateSchPdf [ERROR]: Error occurred: {e}")
    return

  print ("generateSchPdf [OK]: Schematic PDF file exported successfully.")

#============================================================================================= #

def create_final_directory (config_dir, command_dir, target_dir_name, rev, func_name, to_overwrite = True):
  # This will be the root directory for the output files.
  # Extra directories will be created based on the revision, date and sequence number.
  target_dir = None

  # The configured directory has precedence over the command line argument.
  # Check if the config directory is empty.
  if config_dir == "":
    print (f"{func_name} [INFO]: Config directory '{config_dir}' is empty. Using the command line argument.")
    target_dir = command_dir # If it's empty, use the command line argument
  else:
    print (f"{func_name} [INFO]: Config directory '{config_dir}' is not empty. Using the config directory.")
    target_dir = config_dir # Otherwise, use the config directory

  if not os.path.exists (target_dir): # Check if the target directory exists
    print (f"{func_name} [INFO]: Output directory '{target_dir}' does not exist. Creating it now.")
    os.makedirs (target_dir)
  else:
    print (f"{func_name} [INFO]: Output directory '{target_dir}' already exists.")

  #---------------------------------------------------------------------------------------------#

  # Create one more directory based on the revision number.
  rev_directory = f"{target_dir}/R{rev}"

  # Check if the revision directory exists, and create if not.
  if not os.path.exists (rev_directory):
    print (f"{func_name} [INFO]: Revision directory '{rev_directory}' does not exist. Creating it now.")
    os.makedirs (rev_directory)
  
  #---------------------------------------------------------------------------------------------#
  
  not_completed = True
  seq_number = 0
  
  # Now we have to make the date-specific and output-specific directory.
  # This will be the final directory for the output files.
  while not_completed:
    today_date = datetime.now()
    formatted_date = today_date.strftime ("%d-%m-%Y")
    filename_date = today_date.strftime ("%d%m%Y")
    seq_number += 1
    date_directory = f"{rev_directory}/[{seq_number}] {formatted_date}"
    final_directory = f"{date_directory}/{target_dir_name}"

    if not os.path.exists (final_directory):
      print (f"{func_name} [INFO]: Target directory '{final_directory}' does not exist. Creating it now.")
      os.makedirs (final_directory)
      not_completed = False
    else:
      if to_overwrite:
        print (f"{func_name} [INFO]: Target directory '{final_directory}' already exists. Files may be overwritten.")
        not_completed = False
      else:
        print (f"{func_name} [INFO]: Target directory '{final_directory}' already exists. Creating another one.")
        not_completed = True
  
  return final_directory, filename_date

#=============================================================================================#

def generate3D (output_dir, pcb_filename, type, to_overwrite = True):
  # Common base command
  if type == "STEP" or type == "step":
    ddd_export_command = ["kicad-cli", "pcb", "export", "step"]
    type = "STEP"
    extension = "step"
  elif type == "VRML" or type == "vrml":
    ddd_export_command = ["kicad-cli", "pcb", "export", "vrml"]
    type = "VRML"
    extension = "wrl"

  if not check_file_exists (pcb_filename):
    print (f"generate3D [ERROR]: {pcb_filename} does not exist.")
    return

  file_name = extract_pcb_file_name (pcb_filename)
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  
  print (f"generate3D [INFO]: Project name is {project_name} and revision is {info ['rev']}.")
  
  # Check if the ouptut directory exists, and create if not.
  if not os.path.exists (output_dir):
    print (f"generate3D [INFO]: Output directory {output_dir} does not exist. Creating it now.")
    os.makedirs (output_dir)

  rev_directory = f"{output_dir}/R{info ['rev']}"

  if not os.path.exists (rev_directory):
    print (f"generate3D [INFO]: Revision directory {rev_directory} does not exist. Creating it now.")
    os.makedirs (rev_directory)
  
  not_completed = True
  seq_number = 0
  
  while not_completed:
    today_date = datetime.now()
    formatted_date = today_date.strftime ("%d-%m-%Y")
    filename_date = today_date.strftime ("%d%m%Y")
    seq_number += 1
    date_directory = f"{rev_directory}/[{seq_number}] {formatted_date}"
    target_directory = f"{date_directory}/3D"

    if not os.path.exists (target_directory):
      print (f"generate3D [INFO]: Target directory {target_directory} does not exist. Creating it now.")
      os.makedirs (target_directory)
      not_completed = False
    else:
      if to_overwrite:
        print (f"generate3D [INFO]: Target directory {target_directory} already exists.")
        not_completed = False
      else:
        print (f"generate3D [INFO]: Target directory {target_directory} already exists. Creating another one.")
        not_completed = True

  # # Check if the target directory ends with a slash, and add one if not
  # if target_directory [-1] != '/':
  #   target_directory += '/'
  
  seq_number = 1
  not_completed = True
  
  while not_completed:
    file_name = f"{target_directory}/{project_name}-R{info ['rev']}-{type}-{filename_date}-{seq_number}.{extension}"

    if os.path.exists (file_name):
      seq_number += 1
      not_completed = True
    else:
      if type == "STEP":
        full_command = ddd_export_command + \
                      ["--output", f"{target_directory}/{project_name}-R{info ['rev']}-{type}-{filename_date}-{seq_number}.{extension}"] + \
                      ["--force"] + \
                      ["--subst-models"] + \
                      ["--include-tracks"] + \
                      ["--include-zones"] + \
                      [pcb_filename]
        
      elif type == "VRML":
        full_command = ddd_export_command + \
                      ["--output", f"{target_directory}/{project_name}-R{info ['rev']}-{type}-{filename_date}-{seq_number}.{extension}"] + \
                      ["--force"] + \
                      ["--units", "mm"] + \
                      [pcb_filename]
      not_completed = False

  # Run the command
  try:
    subprocess.run (full_command, check = True)
  
  except subprocess.CalledProcessError as e:
    print (f"generate3D [ERROR]: Error occurred: {e}")
    return

  print ("generate3D [OK]: STEP file exported successfully.")

#=============================================================================================#

def generateBom (output_dir, sch_filename, type, to_overwrite = True):
  # Common base command
  bom_export_command = ["kicad-cli", "sch", "export", "bom"]

  if not check_file_exists (sch_filename):
    print (f"generateBom [ERROR]: {sch_filename} does not exist.")
    return

  file_name = extract_pcb_file_name (sch_filename)
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (sch_filename)
  
  print (f"generateBom [INFO]: Project name is {project_name} and revision is {info ['rev']}.")
  
  # Check if the ouptut directory exists, and create if not.
  if not os.path.exists (output_dir):
    print (f"generateBom [INFO]: Output directory {output_dir} does not exist. Creating it now.")
    os.makedirs (output_dir)

  rev_directory = f"{output_dir}/R{info ['rev']}"

  if not os.path.exists (rev_directory):
    print (f"generateBom [INFO]: Revision directory {rev_directory} does not exist. Creating it now.")
    os.makedirs (rev_directory)
  
  not_completed = True
  seq_number = 0
  
  while not_completed:
    today_date = datetime.now()
    formatted_date = today_date.strftime ("%d-%m-%Y")
    filename_date = today_date.strftime ("%d%m%Y")
    seq_number += 1
    date_directory = f"{rev_directory}/[{seq_number}] {formatted_date}"
    target_directory = f"{date_directory}/BoM"

    if not os.path.exists (target_directory):
      print (f"generateBom [INFO]: Target directory {target_directory} does not exist. Creating it now.")
      os.makedirs (target_directory)
      not_completed = False
    else:
      if to_overwrite:
        print (f"generateBom [INFO]: Target directory {target_directory} already exists.")
        not_completed = False
      else:
        print (f"generateBom [INFO]: Target directory {target_directory} already exists. Creating another one.")
        not_completed = True

  # # Check if the target directory ends with a slash, and add one if not
  # if target_directory [-1] != '/':
  #   target_directory += '/'
  
  seq_number = 1
  not_completed = True
  
  while not_completed:
    file_name = f"{target_directory}/{project_name}-R{info ['rev']}-BoM-CSV-{filename_date}-{seq_number}.csv"

    if os.path.exists (file_name):
      seq_number += 1
      not_completed = True
    else:
      full_command = bom_export_command + \
                    ["--output", f"{target_directory}/{project_name}-R{info ['rev']}-BoM-CSV-{filename_date}-{seq_number}.csv"] + \
                    ["--preset", "Group by MPN-DNP"] + \
                    ["--format-preset", "CSV"] + \
                    ["--fields", "${{ITEM_NUMBER}},Reference,Value,Name,Footprint,${{QUANTITY}},${{DNP}},MPN,MFR,Alt MPN"] + \
                    ["--labels", "#,Reference,Value,Name,Footprint,Qty,DNP,MPN,MFR,Alt MPN"] + \
                    ["--group-by", "${{DNP}},MPN"] + \
                    [sch_filename]
      not_completed = False

  # Run the command
  try:
    subprocess.run (full_command, check = True)
  
  except subprocess.CalledProcessError as e:
    print (f"generateBom [ERROR]: Error occurred: {e}")
    return

  print ("generateBom [OK]: BoM file exported successfully.")

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

# =============================================================================================#

def zip_all_files_2 (source_folder, extensions = None, zip_file_name = None):
    """
    Compresses files from a folder into a ZIP file, including only files with specified extensions.

    Args:
        source_folder (str): Path to the folder containing files.
        extensions (list of str, optional): List of file extensions to include (e.g., ['.txt', '.jpg']).
        zip_file_name (str, optional): Name of the ZIP file. If None, will use 'archive.zip'.
    """
    if extensions is None:
        extensions = []  # Include all files if no extensions are specified
    
    if zip_file_name is None:
        zip_file_name = 'archive.zip'  # Default ZIP file name
    
    zip_file_path = os.path.join (source_folder, zip_file_name)
    
    with zipfile.ZipFile (zip_file_path, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk (source_folder):
            for filename in filenames:
                file_path = os.path.join (foldername, filename)
                # Check if the file has one of the specified extensions
                if not extensions or any (filename.endswith (ext) for ext in extensions):
                    # Exclude the ZIP file itself from being added
                    if os.path.abspath (file_path) != os.path.abspath (zip_file_path):
                        zipf.write (file_path, arcname = os.path.relpath (file_path, source_folder))
    
    # print(f"ZIP file created: {zip_file_name}")

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

def delete_files_with_extensions (directory, extensions = None):
    """
    Deletes files in the specified directory with the specified extensions.

    Args:
        directory (str): Path to the directory where the cleanup will occur.
        extensions (str or list of str, optional): Comma-separated string or list of file extensions to delete.
    """
    if extensions is None:
        # print ("No extensions provided. No files will be deleted.")
        return
    
    if isinstance (extensions, str):
        extensions = extensions.split (',')

    # Ensure all extensions are in the form of '.ext'
    extensions = [f".{ext.strip()}" for ext in extensions]

    for filename in os.listdir (directory):
        file_path = os.path.join (directory, filename)
        if os.path.isfile (file_path):
            # Check if file extension matches one of the provided extensions
            if any (filename.endswith (ext) for ext in extensions):
                os.remove (file_path)
                # print(f"Deleted: {filename}")

#=============================================================================================#

def delete_files (directory, include_extensions = None, exclude_extensions = None):
    """
    Deletes files in the specified directory based on the inclusion and exclusion lists of file extensions.

    Args:
        directory (str): Path to the directory where the cleanup will occur.
        include_extensions (list of str, optional): List of file extensions to include for deletion, e.g., ['.txt', '.jpg'].
        exclude_extensions (list of str, optional): List of file extensions to exclude from deletion, e.g., ['.zip'].
    """
    # Ensure inclusion and exclusion lists are properly formatted
    if include_extensions is None:
        include_extensions = []
    # Ensure that include_extensions have leading dots and are unique
    include_extensions = [ext.strip().lower() for ext in include_extensions if ext.startswith('.')]
    
    if exclude_extensions is None:
        exclude_extensions = []
    # Ensure that exclude_extensions have leading dots and are unique
    exclude_extensions = [ext.strip().lower() for ext in exclude_extensions if ext.startswith('.')]

    for filename in os.listdir (directory):
        file_path = os.path.join (directory, filename)
        if os.path.isfile (file_path):
            # Get the file extension
            file_ext = os.path.splitext (filename) [1].lower()
            # Check if file extension is in the inclusion list and not in the exclusion list
            if (not include_extensions or file_ext in include_extensions) and (file_ext not in exclude_extensions):
                os.remove(file_path)
                # print(f"Deleted: {filename}")

#=============================================================================================#

def rename_files (directory, prefix, revision = "", extensions = None):
  if extensions is None:
    extensions = []

  for filename in os.listdir (directory):
    if filename.startswith (prefix) and any (filename.endswith (ext) for ext in extensions):
      # Construct the new filename with the revision tag
      base_name = filename [len (prefix):]  # Remove the prefix part
      new_filename = f"{prefix}-R{revision}{base_name}"
      
      # Full paths for renaming
      old_file_path = os.path.join (directory, filename)
      new_file_path = os.path.join (directory, new_filename)
      
      # Rename the file
      os.rename (old_file_path, new_file_path)
      # print(f"Renamed: {filename} -> {new_filename}")

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

def load_config (config_file, project_file = None):
  global current_config  # Declare the global variable here
  global default_config  # Declare the global variable here

  # Load the default configuration
  print (f"load_config [INFO]: Loading default configuration.")
  default_config = json.loads (DEFAULT_CONFIG_JSON)

  # If a project file is specified, load the configuration from the location of the project file.
  # Else, assume that the configuration file is in the same directory as the cwd.
  if project_file is not None:
    config_file = os.path.join (os.path.dirname (project_file), config_file)

  # Load the configuration from the specified file
  if os.path.exists (config_file):
    print (f"load_config [INFO]: Loading configuration from {config_file}.")
    with open (config_file, 'r') as f:
        current_config = json.load (f)
  else:
    print (f"load_config [WARNING]: A configuration file does not exist. Default values will be used.")
    current_config = default_config

#=============================================================================================#

def test():
  info = extract_info_from_pcb (SAMPLE_PCB_FILE)
  print (info)
  print (f"Revision is {info ['rev']}")

#=============================================================================================#

def parseArguments():
  parser = argparse.ArgumentParser (description = "KiExport: Tool to export manufacturing files from KiCad PCB projects.")
  
  parser.add_argument('-v', '--version', action = 'version', version = f'{APP_VERSION}', help = "Show the version of the tool and exit.")

  subparsers = parser.add_subparsers (dest = "command", help = "Available commands.")

  # Subparser for the Gerber export command
  # Example: python .\kiexport.py gerbers -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  gerbers_parser = subparsers.add_parser ("gerbers", help = "Export Gerber files.")
  gerbers_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  gerbers_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Gerber files to.")

  # Subparser for the Drills export command
  # Example: python .\kiexport.py drills -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  drills_parser = subparsers.add_parser ("drills", help = "Export Drill files.")
  drills_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  drills_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Drill files to.")

  # Subparser for the Position file export command
  # Example: python .\kiexport.py positions -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  positions_parser = subparsers.add_parser ("positions", help = "Export Position files.")
  positions_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  positions_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Position files to.")

  # Subparser for the PCB PDF export command
  # Example: python .\kiexport.py pcb_pdf -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  pcb_pdf_parser = subparsers.add_parser ("pcb_pdf", help = "Export PCB PDF files.")
  pcb_pdf_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  pcb_pdf_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the PCB PDF files to.")

  # Subparser for the Schematic PDF export command
  # Example: python .\kiexport.py sch_pdf -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_sch"
  sch_pdf_parser = subparsers.add_parser ("sch_pdf", help = "Export schematic PDF files.")
  sch_pdf_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_sch file.")
  sch_pdf_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Schematic PDF files to.")

  # Subparser for the 3D file export command
  # Example: python .\kiexport.py ddd -t "VRML" -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  ddd_parser = subparsers.add_parser ("ddd", help = "Export 3D files.")
  ddd_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  ddd_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the 3D files to.")
  ddd_parser.add_argument ("-t", "--type", required = True, help = "The type of file to generate. Can be STEP or VRML.")

  # Subparser for the BoM file export command
  # Example: python .\kiexport.py bom -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  bom_parser = subparsers.add_parser ("bom", help = "Export BoM files.")
  bom_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_sch file.")
  bom_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the BoM files to.")
  bom_parser.add_argument ("-t", "--type", help = "The type of file to generate. Default is CSV.")
  
  test_parser = subparsers.add_parser ("test", help = "Internal test function.")

  # Parse arguments
  args = parser.parse_args()
  
  printInfo()

  if args.command is None:
    print (color.red ("Looks like you forgot to specify any inputs. Time to RTFM."))
    print()
    parser.print_help()
    return

  # Check if we received an input file
  if args.input_filename is not None:
    load_config (config_file = "kiexport.json", project_file = args.input_filename)
  else:
    load_config (config_file = "kiexport.json")

  if args.command == "-v" or args.command == "--version":
    print (f"KiExport v{APP_VERSION}")
    return

  if args.command == "gerbers":
    generateGerbers (args.output_dir, args.input_filename)

  elif args.command == "drills":
    generateDrills (args.output_dir, args.input_filename)
  
  elif args.command == "positions":
    generatePositions (args.output_dir, args.input_filename)
  
  elif args.command == "pcb_pdf":
    generatePcbPdf (args.output_dir, args.input_filename)

  elif args.command == "sch_pdf":
    generateSchPdf (args.output_dir, args.input_filename)

  elif args.command == "bom":
    generateBom (args.output_dir, args.input_filename, args.type)
  
  elif args.command == "ddd":
    generate3D (args.output_dir, args.input_filename, args.type)

  elif args.command == "test":
    test()
    
  else:
    parser.print_help()

#=============================================================================================#

def printInfo():
  print ("")
  print (f"KiExport v{APP_VERSION}")
  print ("CLI tool to export design and manufacturing files from KiCad projects.")
  print ("Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)")
  print ("")

#=============================================================================================#

def main():
  parseArguments()

#=============================================================================================#

if __name__ == "__main__":
  main()

#=============================================================================================#
