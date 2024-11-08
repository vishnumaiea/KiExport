
#=============================================================================================#

# KiExport
# Tool to export manufacturing files from KiCad PCB projects.
# Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)
# Version: 0.0.26
# Last Modified: +05:30 23:05:17 PM 08-11-2024, Friday
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
import pymupdf

#=============================================================================================#

APP_NAME = "KiExport"
APP_VERSION = "0.0.26"

SAMPLE_PCB_FILE = "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"

current_config = None
default_config = None

DEFAULT_CONFIG_JSON = '''
{
  "name": "KiExport.JSON",
  "description": "Configuration file for KiExport",
  "filetype": "json",
  "version": "1.2",
  "project_name": "Mitayi-Pico-RP2040",
  "commands": ["gerbers", "drills", "sch_pdf", "bom", "ibom", "pcb_pdf", "positions", ["ddd", "STEP"], ["ddd", "VRML"]],
  "kicad_python_path": "C:\\\\Program Files\\\\KiCad\\\\8.0\\\\bin\\\\python.exe",
  "ibom_path": "C:\\\\Users\\\\vishn\\\\Documents\\\\KiCad\\\\8.0\\\\3rdparty\\\\plugins\\\\org_openscopeproject_InteractiveHtmlBom\\\\generate_interactive_bom.py",
  "data": {
    "gerbers": {
      "--output_dir": "Export",
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
      "--output_dir": "Export",
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
        "--output_dir": "Export",
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
      },
      "iBoM": {
        "--output_dir": "Export",
        "--show-dialog": false,
        "--dark-mode": true,
        "--hide-pads": false,
        "--show-fabrication": false,
        "--hide-silkscreen": false,
        "--highlight-pin1": "all",
        "--no-redraw-on-drag": false,
        "--board-rotation": "0",
        "--offset-back-rotation": "0",
        "--checkboxes": "Source,Placed",
        "--bom-view": "left-right",
        "--layer-view": "FB",
        "--no-compression": false,
        "--no-browser": true,
        "--include-tracks": true,
        "--include-nets": true,
        "--sort-order": "C,R,L,D,U,Y,X,F,SW,A,~,HS,CNN,J,P,NT,MH",
        "--blacklist": false,
        "--no-blacklist-virtual": false,
        "--blacklist-empty-value": false,
        "--netlist-file": false,
        "--extra-data-file": false,
        "--extra-fields": false,
        "--show-fields": "Value,Footprint",
        "--group-fields": "Value,Footprint",
        "--normalize-field-case": false,
        "--variant-fields": false,
        "--variants-whitelist": false,
        "--dnp-field": false
      }
    },
    "sch_pdf": {
      "--output_dir": "Export",
      "--drawing-sheet": false,
      "--theme": "User",
      "--black-and-white": false,
      "--exclude-drawing-sheet": false,
      "--exclude-pdf-property-popups": false,
      "--no-background-color": false,
      "--pages": false
    },
    "pcb_pdf": {
      "--output_dir": "Export",
      "--layers": ["F.Cu","B.Cu","F.Paste","B.Paste","F.Silkscreen","B.Silkscreen","F.Mask","B.Mask","User.Drawings","User.Comments","Edge.Cuts","F.Courtyard","B.Courtyard","F.Fab","B.Fab"],
      "kie_common_layers": ["Edge.Cuts"],
      "--drawing-sheet": false,
      "--mirror": false,
      "--exclude-refdes": false,
      "--exclude-value": false,
      "--include-border-title": true,
      "--negative": false,
      "--black-and-white": false,
      "--theme": "User",
      "--drill-shape-opt": 2,
      "kie_single_file": false
    },
    "positions": {
      "--output_dir": "Export",
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
        "--output_dir": "Export",
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
        "--output_dir": "Export",
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
    def __call__ (self, text, color):
        return f"{COLORS[color]}{text}{COLORS['reset']}"
    
    def __getattr__ (self, color):
        if color in COLORS:
            return lambda text: self(text, color)
        raise AttributeError (f"Color '{color}' is not supported.")

# Create an instance of the Colorize class
color = _color()

#=============================================================================================#

def generateiBoM (output_dir = None, pcb_filename = None, extra_args = None):
  """
  Runs the KiCad iBOM Python script on a specified PCB file.

  Args:
    pcb_filename (str): Path to the KiCad PCB file (.kicad_pcb).
    output_dir (str): Directory to save the output files. Defaults to the PCB file's directory.
    extra_args (list): Additional command-line arguments for customization (optional).

  Returns:
    str: Path to the generated iBOM HTML file.
  """

  # Read the paths.
  kicad_python_path = f'"{current_config.get ("kicad_python_path", default_config ["kicad_python_path"])}"'
  ibom_path = f'"{current_config.get ("ibom_path", default_config ["ibom_path"])}"'

  # Check if the KiCad Python path exists.
  if not os.path.isfile (kicad_python_path):
    raise FileNotFoundError (f"generateiBoM() [ERROR]: The KiCad Python path '{kicad_python_path}' does not exist.")
  else:
    kicad_python_path = f'"{current_config.get ("kicad_python_path", default_config ["kicad_python_path"])}"'

  # Check if the iBOM script path exists.
  if not os.path.isfile (ibom_path):
    raise FileNotFoundError (f"generateiBoM() [ERROR]: The iBOM path '{ibom_path}' does not exist.")
  else:
    ibom_path = f'"{current_config.get ("ibom_path", default_config ["ibom_path"])}"'
  
  # Construct the iBOM command.
  ibom_export_command = [kicad_python_path, ibom_path]

  #---------------------------------------------------------------------------------------------#
  
  # Ensure PCB file exists.
  if not os.path.isfile (pcb_filename):
    raise FileNotFoundError (f"generateiBoM() [ERROR]: The PCB file '{pcb_filename}' does not exist.")
  
  #---------------------------------------------------------------------------------------------#

  file_name = extract_pcb_file_name (pcb_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen

  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  
  print (f"generateiBoM() [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")
  # ibom_filename = f"{project_name}-R{info ['rev']}-HTML-BoM-{filename_date}.html"

  #---------------------------------------------------------------------------------------------#

  file_path = os.path.abspath (pcb_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("bom", {}).get ("iBoM").get ("--output_dir", default_config ["data"]["bom"]["iBoM"]["--output_dir"])
  od_from_cli = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "BoM", info ["rev"], "generateiBoM")

  #---------------------------------------------------------------------------------------------#

  # Form the initial part of the command
  
  full_command = []
  full_command.extend (ibom_export_command) # Add the base command
  
  seq_number = 1
  not_completed = True
  
  # Create the output file name.
  while not_completed:
    file_name = f"{final_directory}/{project_name}-R{info ['rev']}-BoM-HTML-{filename_date}-{seq_number}.html" # Extension needed here

    if os.path.exists (file_name):
      seq_number += 1
      not_completed = True
    else:
      full_command.append ("--dest-dir")
      full_command.append (f'"{final_directory}"') # Add the output file name with double quotes around it
      full_command.append ("--name-format")
      file_name = f"{project_name}-R{info ['rev']}-BoM-HTML-{filename_date}-{seq_number}" # No extension needed
      full_command.append (f'"{file_name}"')
      break
  
  #---------------------------------------------------------------------------------------------#

  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("bom", {}).get ("iBoM")

  # Add the remaining arguments.
  # Check if the argument list is not an empty dictionary.
  if arg_list:
    for key, value in arg_list.items():
      if key.startswith ("--"): # Only fetch the arguments that start with "--"
        if key == "--output_dir": # Skip the --output_dir argument, sice we already added it
          continue

        elif key == "--name-format": # Skip the --name-format argument
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
  print ("generateBom [INFO]: Running command: ", color.blue (' '.join (full_command)))

  #---------------------------------------------------------------------------------------------#

  # Run the iBOM script with error handling
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
    print (color.green (f"generateiBoM() [INFO]: Interactive HTML BoM generated successfully."))

  except subprocess.CalledProcessError as e:
    print (color.red (f"generateiBoM() [ERROR]: Error during HTML BoM generation: {e}"))
    print (color.red (f"generateiBoM() [INFO]: Make sure the 'Interactive HTML BoM' application is installed and available on the PATH."))

  except Exception as e:
    print (color.red (f" generateiBoM() [ERROR]: An unexpected error occurred: {e}"))

#=============================================================================================#

def merge_pdfs (folder_path, output_file):
  """
  Merges PDF files in a folder and creates a TOC based on file names.

  Args:
    folder_path (str): Path to the folder containing PDF files.
    output_file (str): Name of the output PDF file.
  """
  try:
    # List all PDF files in the specified folder.
    pdf_files = [f for f in os.listdir (folder_path) if f.endswith ('.pdf')]
    
    if not pdf_files:
      print (f"merge_pdfs() [WARNING]: No PDF files found in the specified folder.")
      return

    # pdf_files.sort()  # Optional: sort the files alphabetically
    doc = pymupdf.open()  # Create a new PDF document
    toc = []  # List to hold the Table of Contents entries

    # Add each PDF to the document and create TOC entries
    for pdf in pdf_files:
      pdf_path = os.path.join (folder_path, pdf)
      try:
        with pymupdf.open (pdf_path) as pdf_doc:
          start_page = doc.page_count  # Get the starting page number
          doc.insert_pdf (pdf_doc)  # Merge the PDF
          toc.append ((1, pdf [:-4], start_page + 1))  # Add TOC entry

      except Exception as e:
        print (color.red (f"merge_pdfs() [ERROR]: Error processing file {pdf}: {e}"))

    # Set the Table of Contents
    doc.set_toc (toc)

    # Save the merged document
    output_path = os.path.join (folder_path, output_file)
    doc.save (output_path)
    doc.close()

    # # Delete original PDF files.
    # for pdf in pdf_files:
    #   os.remove (os.path.join (folder_path, pdf))

    # print (f"Merged PDF created: {output_path}")
    # print ("Original PDF files have been deleted.")

  except PermissionError:
    print (color.red ("merge_pdfs() [ERROR]: Unable to access the specified folder or files."))
  except Exception as e:
    print (color.red (f"merge_pdfs() [ERROR]: {e}"))

#=============================================================================================#

def generateGerbers (output_dir, pcb_filename, to_overwrite = True):
  # Generate the drill files first if specified
  kie_include_drill = current_config.get ("data", {}).get ("gerbers", {}).get ("kie_include_drill", default_config ["data"]["gerbers"]["kie_include_drill"])

  # Check if the value is boolean and then true or false
  if isinstance (kie_include_drill, bool):
    kie_include_drill = str (kie_include_drill).lower()

  if kie_include_drill == "true":
    kie_include_drill = True
  elif kie_include_drill == "false":
    kie_include_drill = False

  if kie_include_drill == True:
    generateDrills (output_dir, pcb_filename)
  
  #---------------------------------------------------------------------------------------------#
  
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
  print (f"generateGerbers [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")
  
  #---------------------------------------------------------------------------------------------#
  
  file_path = os.path.abspath (pcb_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("gerbers", {}).get ("--output_dir", default_config ["data"]["gerbers"]["--output_dir"])
  od_from_cli = output_dir  # The output directory specified by the command line argument

  # Get the final directory path.
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "Gerber", info ["rev"], "generateGerbers")

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

  files_to_include = [".gbr", ".gbrjob"]

  if kie_include_drill:
    files_to_include.extend ([".drl", ".ps", ".pdf"])
  
  # Sequentially name and create the zip files.
  while not_completed:
    zip_file_name = f"{project_name}-R{info ['rev']}-Gerber-{filename_date}-{seq_number}.zip"

    if os.path.exists (f"{final_directory}/{zip_file_name}"):
      seq_number += 1
    else:
      # zip_all_files (final_directory, f"{final_directory}/{zip_file_name}")
      zip_all_files_2 (final_directory, files_to_include, zip_file_name)
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
  print (f"generateDrills [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")
  
  #-------------------------------------------------------------------------------------------#

  file_path = os.path.abspath (pcb_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the target directory name from the config file
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("drills", {}).get ("--output_dir", default_config ["data"]["drills"]["--output_dir"])
  od_from_cli = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "Gerber", info ["rev"], "generateDrills")

  # Check if the final directory ends with a slash, and add one if not.
  if final_directory [-1] != "/":
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
    print (color.red (f"generatePositions [ERROR]: '{pcb_filename}' does not exist."))
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (pcb_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen
  
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  print (f"generatePositions [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")
  
  #---------------------------------------------------------------------------------------------#

  file_path = os.path.abspath (pcb_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("positions", {}).get ("--output_dir", default_config ["data"]["positions"]["--output_dir"])
  od_from_cli = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "Assembly", info ["rev"], "generatePositions")
  
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
    print (color.yellow (f"generatePositions [INFO]: No sides specified. Using both sides."))
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
        print (f"generatePositions [INFO]: Running command: {color.blue (command_string)}")
        subprocess.run (command_string, check = True)
      except subprocess.CalledProcessError as e:
        print (color.red (f"generatePositions [ERROR]: Error occurred while generating the files."))
        return

  print (color.green ("generatePositions [OK]: Position files exported successfully."))
  
  #---------------------------------------------------------------------------------------------#
  
  # Rename the files by adding Revision after the project name.
  rename_files (final_directory, project_name, info ['rev'], [".csv"])
  
  #---------------------------------------------------------------------------------------------#
  
  seq_number = 1
  not_completed = True

  files_to_include = [".csv"]
  
  # Sequentially name and create the zip files.
  while not_completed:
    zip_file_name = f"{project_name}-R{info ['rev']}-Position-Files-{filename_date}-{seq_number}.zip"

    if os.path.exists (f"{final_directory}/{zip_file_name}"):
      seq_number += 1
    else:
      # zip_all_files (final_directory, f"{final_directory}/{zip_file_name}")
      zip_all_files_2 (final_directory, files_to_include, zip_file_name)
      print (f"generatePositions [OK]: ZIP file '{color.magenta (zip_file_name)}' created successfully.")
      not_completed = False

#=============================================================================================#

def generatePcbPdf (output_dir, pcb_filename, to_overwrite = True):
  # Common base command
  pcb_pdf_export_command = ["kicad-cli", "pcb", "export", "pdf"]

  # Check if the pcb file exists
  if not check_file_exists (pcb_filename):
    print (color.red (f"generatePcbPdf [ERROR]: '{pcb_filename}' does not exist."))
    return

  #---------------------------------------------------------------------------------------------#

  file_name = extract_pcb_file_name (pcb_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen
  
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  print (f"generatePcbPdf [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")
  
  #---------------------------------------------------------------------------------------------#

  file_path = os.path.abspath (pcb_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("pcb_pdf", {}).get ("--output_dir", default_config ["data"]["pcb_pdf"]["--output_dir"])
  od_from_cli = output_dir  # The output directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "PCB", info ["rev"], "generatePcbPdf")

  #---------------------------------------------------------------------------------------------#
  
  # Delete the existing files in the output directory
  delete_files (final_directory, include_extensions = [".pdf", ".ps"])

  #---------------------------------------------------------------------------------------------#
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("pcb_pdf", {})

  # Check the number of technical layers to export. This is not the number of copper layers.
  layer_count = len (arg_list.get ("--layers", []))

  if layer_count <= 0:
    print (color.red (f"generatePcbPdf [ERROR]: No layers specified for export."))
    return

  # Get the number of common layers to include in each of the PDF.
  # common_layer_count = len (arg_list.get ("kie_common_layers", []))

  seq_number = 1
  not_completed = True
  base_command = []
  base_command.extend (pcb_pdf_export_command) # Add the base command
  
  for i in range (layer_count):
    full_command = base_command [:]
    # Get the arguments.
    if arg_list: # Check if the argument list is not an empty dictionary.
      for key, value in arg_list.items():
        if key.startswith ("--"): # Only fetch the arguments that start with "--"
          if key == "--output_dir": # Skip the --output_dir argument, sice we already added it
            continue
          elif key == "--layers":
            layer_name = arg_list ["--layers"][i] # Get a layer name from the layer list
            layer_name = layer_name.replace (".", "_") # Replace dots with underscores
            layer_name = layer_name.replace (" ", "_") # Replace spaces with underscores

            full_command.append ("--output")
            full_command.append (f'"{final_directory}/{project_name}-R{info ["rev"]}-{layer_name}.pdf"') # This is the ouput file name, and not a directory name

            layer_name = arg_list ["--layers"][i] # Get a layer name from the layer list
            layer_list = [f"{layer_name}"]  # Now create a list with the first item as the layer name
            common_layer_list = arg_list ["kie_common_layers"]  # Add the common layers
            layer_list.extend (common_layer_list) # Now combine the two lists
            layers_csv = ",".join (layer_list) # Convert the list to a comma-separated string
            full_command.append (key)
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

    full_command.append (f'"{pcb_filename}"')
    print ("generatePcbPdf [INFO]: Running command: ", color.blue (' '.join (full_command)))

      # Run the command
    try:
      full_command = ' '.join (full_command) # Convert the list to a string
      subprocess.run (full_command, check = True)
      # print (color.green ("generatePcbPdf [OK]: PCB PDF files exported successfully."))
    
    except subprocess.CalledProcessError as e:
      print (color.red (f"generatePcbPdf [ERROR]: Error occurred: {e}"))
      continue
  
  #---------------------------------------------------------------------------------------------#
  
  # # Generate a single file if specified
  # kie_single_file = current_config.get ("data", {}).get ("pcb_pdf", {}).get ("kie_single_file", default_config ["data"]["pcb_pdf"]["kie_single_file"])

  # # Check if the value is boolean and then true or false
  # if isinstance (kie_single_file, bool):
  #   kie_single_file = str (kie_single_file).lower()

  # if kie_single_file == "true":
  #   kie_single_file = True
  # elif kie_single_file == "false":
  #   kie_single_file = False

  # if kie_single_file == True:
  #   full_command.append (f'"{pcb_filename}"')
  
  #---------------------------------------------------------------------------------------------#

  # Merge all the PDFs into one file
  merged_pdf_filename = f"{project_name}-R{info ['rev']}-PCB-PDF-All-{filename_date}-{seq_number}.pdf"
  merge_pdfs (final_directory, merged_pdf_filename)

  #---------------------------------------------------------------------------------------------#

  print (color.green ("generatePcbPdf [OK]: PCB PDF files exported successfully."))

  #---------------------------------------------------------------------------------------------#

  seq_number = 1
  not_completed = True

  files_to_include = [".pdf"]
  
  # Sequentially name and create the zip files.
  while not_completed:
    zip_file_name = f"{project_name}-R{info ['rev']}-PCB-PDF-{filename_date}-{seq_number}.zip"

    if os.path.exists (f"{final_directory}/{zip_file_name}"):
      seq_number += 1
    else:
      # zip_all_files (final_directory, f"{final_directory}/{zip_file_name}")
      zip_all_files_2 (final_directory, files_to_include, zip_file_name)
      print (f"generatePcbPdf [OK]: ZIP file '{color.magenta (zip_file_name)}' created successfully.")
      print()
      not_completed = False

#=============================================================================================#

def generateSchPdf (output_dir, sch_filename, to_overwrite = True):
  global current_config  # Access the global config
  global default_config  # Access the global config

  # Common base command
  sch_pdf_export_command = ["kicad-cli", "sch", "export", "pdf"]

  # Check if the input file exists
  if not check_file_exists (sch_filename):
    print (color.red (f"generateSchPdf [ERROR]: '{sch_filename}' does not exist."))
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (sch_filename) # Extract information from the input file
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen

  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (sch_filename) # Extract basic information from the input file

  print (f"generateSchPdf [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")

  #---------------------------------------------------------------------------------------------#

  file_path = os.path.abspath (sch_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("sch_pdf", {}).get ("--output_dir", default_config ["data"]["sch_pdf"]["--output_dir"])
  od_from_cli = output_dir  # The output directory specified by the command line argument

  # Get the final directory path.
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "SCH", info ["rev"], "generateSchPdf")
  
  #---------------------------------------------------------------------------------------------#
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("sch_pdf", {})

  full_command = []
  full_command.extend (sch_pdf_export_command) # Add the base command

  seq_number = 1
  not_completed = True
  
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
  print ("generateSchPdf [INFO]: Running command: ", color.blue (' '.join (full_command)))

  #---------------------------------------------------------------------------------------------#
  
  # Run the command
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
  
  except subprocess.CalledProcessError as e:
    print (color.red (f"generateSchPdf [ERROR]: Error occurred: {e}"))
    return

  print (color.green ("generateSchPdf [OK]: Schematic PDF file exported successfully."))

#=============================================================================================#

def generate3D (output_dir, pcb_filename, type = "STEP", to_overwrite = True):
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
    print (color.red (f"generate3D [ERROR]: '{pcb_filename}' does not exist."))
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (pcb_filename) # Extract information from the input file
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen

  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (pcb_filename)
  
  print (f"generate3D [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")

  #---------------------------------------------------------------------------------------------#

  file_path = os.path.abspath (pcb_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("ddd", {}).get (type, {}).get ("--output_dir", default_config ["data"]["ddd"][type]["--output_dir"])
  od_from_cli = output_dir  # The directory specified by the command line argument

  # Get the final directory path
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "3D", info ["rev"], "generate3D")

  #---------------------------------------------------------------------------------------------#
  
  full_command = []
  full_command.extend (ddd_export_command) # Add the base command
  
  seq_number = 1
  not_completed = True
  
  # Generate the file name.
  while not_completed:
    file_name = f"{final_directory}/{project_name}-R{info ['rev']}-{type}-{filename_date}-{seq_number}.{extension}"

    if os.path.exists (file_name):
      seq_number += 1
      not_completed = True
    else:
      full_command.append ("--output")
      full_command.append (f'"{file_name}"') # Add the output file name with double quotes around it
      break
  
  #---------------------------------------------------------------------------------------------#
  
  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("ddd", {}).get (type)

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
  print ("generate3D [INFO]: Running command: ", color.blue (' '.join (full_command)))

  #---------------------------------------------------------------------------------------------#
  
  # Run the command
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
  
  except subprocess.CalledProcessError as e:
    print (color.red (f"generate3D [ERROR]: Error occurred: {e}"))
    return

  print (color.green (f"generate3D [OK]: {type} file exported successfully."))

#=============================================================================================#

def generateBom (output_dir, sch_filename, type, to_overwrite = True):
  # Common base command
  bom_export_command = ["kicad-cli", "sch", "export", "bom"]

  # Check if the input file exists
  if not check_file_exists (sch_filename):
    print (color.red (f"generateBom [ERROR]: '{sch_filename}' does not exist."))
    return

  #---------------------------------------------------------------------------------------------#
  
  file_name = extract_pcb_file_name (sch_filename)
  file_name = file_name.replace (" ", "-") # If there are whitespace characters in the project name, replace them with a hyphen
  
  project_name = extract_project_name (file_name)
  info = extract_info_from_pcb (sch_filename)
  
  print (f"generateBom [INFO]: Project name is '{color.magenta (project_name)}' and revision is {color.magenta ('R')}{color.magenta (info ['rev'])}.")

  #---------------------------------------------------------------------------------------------#
  
  file_path = os.path.abspath (sch_filename) # Get the absolute path of the file.

  # Get the directory path of the file and save it as the project directory.
  # All other export directories will be relative to the project directory.
  project_dir = os.path.dirname (file_path)
  
  # Read the output directory name from the config file.
  od_from_config = project_dir + "/" + current_config.get ("data", {}).get ("bom", {}).get ("CSV").get ("--output_dir", default_config ["data"]["bom"]["CSV"]["--output_dir"])
  od_from_cli = output_dir  # The output directory specified by the command line argument

  # Get the final directory path.
  final_directory, filename_date = create_final_directory (od_from_config, od_from_cli, "BoM", info ["rev"], "generateBom")
  
  #---------------------------------------------------------------------------------------------#
  
  full_command = []
  full_command.extend (bom_export_command) # Add the base command
  
  seq_number = 1
  not_completed = True
  
  # Create the output file name.
  while not_completed:
    file_name = f"{final_directory}/{project_name}-R{info ['rev']}-BoM-CSV-{filename_date}-{seq_number}.csv"

    if os.path.exists (file_name):
      seq_number += 1
      not_completed = True
    else:
      full_command.append ("--output")
      full_command.append (f'"{file_name}"') # Add the output file name with double quotes around it
      break

  #---------------------------------------------------------------------------------------------#

  # Get the argument list from the config file.
  arg_list = current_config.get ("data", {}).get ("bom", {}).get ("CSV")

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
  print ("generateBom [INFO]: Running command: ", color.blue (' '.join (full_command)))

  #---------------------------------------------------------------------------------------------#
  
  # Run the command
  try:
    full_command = ' '.join (full_command) # Convert the list to a string
    subprocess.run (full_command, check = True)
  
  except subprocess.CalledProcessError as e:
    print (color.red (f"generateBom [ERROR]: Error occurred: {e}"))
    return

  print (color.green ("generateBom [OK]: BoM file exported successfully."))

#============================================================================================= #

def create_final_directory (dir_from_config, dir_from_cli, target_dir_name, rev, func_name, to_overwrite = True):
  # This will be the root directory for the output files.
  # Extra directories will be created based on the revision, date and sequence number.
  target_dir = None

  # The command line directory has precedence over the  configured directory.
  if dir_from_cli == "":
    print (f"{func_name} [INFO]: CLI directory '{color.magenta (dir_from_config)}' is empty. Using the configured directory.")
    target_dir = dir_from_cli # If it's empty, use the configured directory
  else:
    print (f"{func_name} [INFO]: CLI directory '{color.magenta (dir_from_config)}' is not empty. Using the CLI directory.")
    target_dir = dir_from_config # Otherwise, use the command line argument

  if not os.path.exists (target_dir): # Check if the target directory exists
    print (f"{func_name} [INFO]: Output directory '{color.magenta (target_dir)}' does not exist. Creating it now.")
    os.makedirs (target_dir)
  else:
    print (f"{func_name} [INFO]: Output directory '{color.magenta (target_dir)}' already exists.")

  #---------------------------------------------------------------------------------------------#

  # Create one more directory based on the revision number.
  rev_directory = f"{target_dir}/R{rev}"

  # Check if the revision directory exists, and create if not.
  if not os.path.exists (rev_directory):
    print (f"{func_name} [INFO]: Revision directory '{color.magenta (rev_directory)}' does not exist. Creating it now.")
    os.makedirs (rev_directory)
  
  #---------------------------------------------------------------------------------------------#
  
  not_completed = True
  seq_number = 0
  
  # Now we have to make the date-specific and output-specific directory.
  # This will be the final directory for the output files.
  while not_completed:
    today_date = datetime.now()
    # formatted_date = today_date.strftime ("%d-%m-%Y")
    formatted_date = today_date.strftime ("%Y-%m-%d")
    filename_date = today_date.strftime ("%d%m%Y")
    seq_number += 1
    # date_directory = f"{rev_directory}/[{seq_number}] {formatted_date}"
    date_directory = f"{rev_directory}/{formatted_date}"
    final_directory = f"{date_directory}/{target_dir_name}"

    if not os.path.exists (final_directory):
      print (f"{func_name} [INFO]: Target directory '{color.magenta (final_directory)}' does not exist. Creating it now.")
      os.makedirs (final_directory)
      not_completed = False
    else:
      if to_overwrite:
        print (f"{func_name} [INFO]: Target directory '{color.magenta (final_directory)}' already exists. Files may be overwritten.")
        not_completed = False
      else:
        print (f"{func_name} [INFO]: Target directory '{color.magenta (final_directory)}' already exists. Creating another one.")
        not_completed = True
  
  return final_directory, filename_date

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
  """
  Rename files in the specified directory. Only files starting with the prefix will be renamed.
  You can also specify the revision number to be used when the file is renamed. The renaming will only
  be applied to the files with the listed extensions. If no extensions are given,
  all files will be renamed.

  Args:
      directory (str): The directory of the files to rename.
      prefix (str): The prefix of the files to be renamed. Only these files will be renamed.
      revision (str, optional): The revision tag. For example, "0.1". Defaults to "".
      extensions (list of str, optional): The list of extensions. Only these files will be renamed. Defaults to None.
  """
  
  if extensions is None:
    extensions = [] # All file types will be considered if no extension filter is specified

  for filename in os.listdir (directory):
    # Check if the filename starts with the prefix and ends with a valid extension (or any extension if none specified)
    if filename.startswith (prefix) and (not extensions or any (filename.endswith (ext) for ext in extensions)):
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

def load_config (config_file = None):
  """
  Loads the JSON configuration file. If no file is provided, it uses the default configuration.

  Args:
    config_file (str, optional): Path to the configuration file. Can be relative or absolute. Defaults to None.
  """
  
  global current_config  # Declare the global variable here
  global default_config  # Declare the global variable here

  # Load the default configuration.
  # This is required to load values that are missing in the user-provided configuration.
  print (f"load_config [INFO]: Loading default configuration.")
  default_config = json.loads (DEFAULT_CONFIG_JSON)

  #---------------------------------------------------------------------------------------------#
  
  if config_file is not None:
    # Load the configuration from the specified file.
    if os.path.exists (config_file):
      print (f"load_config [INFO]: Loading configuration from '{color.magenta (config_file)}'.")
      with open (config_file, 'r') as f:
          current_config = json.load (f)
          # TODO: Check the JSON configuration file version and warn about consequences.
    else:
      print (color.yellow (f"load_config [WARNING]: The provided configuration file '{config_file}' does not exist. Default values will be used."))
      current_config = default_config

  else:
    # Use the default configuration.
    print (f"load_config [INFO]: Using default configuration.")
    current_config = default_config

#=============================================================================================#

def run (config_file):
  print (f"run [INFO]: Running KiExport with configuration file '{color.magenta (config_file)}'.")
  load_config (config_file)

  #---------------------------------------------------------------------------------------------#

  valid_commands = ["gerbers", "drills", "sch_pdf", "bom", "ibom", "pcb_pdf", "positions", "ddd"]

  # Get the argument list from the config file.
  user_cmd_list = current_config.get ("commands", [])
  cmd_strings = []
  cmd_lists = []

  if not user_cmd_list:
    print (color.red ("run [ERROR]: No list of commands specified in the configuration file."))
    return
  else:
    cmd_count = 0

    # Check if the commands are valid
    for cmd in user_cmd_list:
      # If cmd is a string, validate directly
      if isinstance (cmd, str) and cmd in valid_commands:
        cmd_strings.append (cmd)
        cmd_count += 1

      # If cmd is a list, validate the first item as a command
      elif isinstance (cmd, list) and cmd [0] in valid_commands:
        cmd_lists.append (cmd)
        cmd_count += 1

    if cmd_count == 0:
      print (color.red ("run [ERROR]: No valid commands specified in the configuration file."))
      return
    else:
      # Print the validated commands
      print (f"run [INFO]: Running the following commands: {color.green (user_cmd_list)}, {color.green (cmd_count)}.")
  
  #---------------------------------------------------------------------------------------------#

  # Find the absolute path to the config file directory.
  config_path = os.path.abspath (config_file)
  project_dir = os.path.dirname (config_path)
  project_name = current_config.get ("project_name")

  pcb_filename = project_name + ".kicad_pcb"
  sch_filename = project_name + ".kicad_sch"

  pcb_file_path = project_dir + "\\" + pcb_filename
  sch_file_path = project_dir + "\\" + sch_filename

  # Print the file names.
  print (f"run [INFO]: Project Directory: {color.magenta (project_dir)}")
  print (f"run [INFO]: PCB File: {color.magenta (pcb_filename)}")
  print (f"run [INFO]: Schematic File: {color.magenta (sch_filename)}")
  print()

  # Check if the file exists.
  if not os.path.isfile (pcb_file_path):
    print (color.yellow (f"run [WARNING]: The PCB file '{pcb_file_path}' does not exist."))
    print (color.yellow ("run [WARNING]: Commands that require the PCB file won't be executed."))
  
  if not os.path.isfile (sch_file_path):
    print (color.yellow (f"run [WARNING]: The Schematic file '{sch_file_path}' does not exist."))
    print (color.yellow ("run [WARNING]: Commands that require the Schematic file won't be executed."))

  # return

  #---------------------------------------------------------------------------------------------#

  # Process the commands without any arguments or modifiers.
  for cmd in cmd_strings:
    if cmd == "gerbers":
      output_dir = current_config.get ("data", {}).get ("gerbers", {}).get ("--output_dir", default_config ["data"]["gerbers"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateGerbers (output_dir, pcb_file_path)

    elif cmd == "drills":
      output_dir = current_config.get ("data", {}).get ("drills", {}).get ("--output_dir", default_config ["data"]["drills"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateDrills (output_dir, pcb_file_path)

    elif cmd == "sch_pdf":
      output_dir = current_config.get ("data", {}).get ("sch_pdf", {}).get ("--output_dir", default_config ["data"]["sch_pdf"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateSchPdf (output_dir, sch_file_path)

    elif cmd == "bom":
      output_dir = current_config.get ("data", {}).get ("bom", {}).get ("CSV", {}).get ("--output_dir", default_config ["data"]["bom"]["CSV"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateBom (output_dir, sch_file_path, "CSV")

    elif cmd == "ibom":
      output_dir = current_config.get ("data", {}).get ("bom", {}).get ("iBoM", {}).get ("--output_dir", default_config ["data"]["bom"]["iBoM"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateiBoM (output_dir, pcb_file_path)

    elif cmd == "pcb_pdf":
      output_dir = current_config.get ("data", {}).get ("pcb_pdf", {}).get ("--output_dir", default_config ["data"]["pcb_pdf"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generatePcbPdf (output_dir, pcb_file_path)

    elif cmd == "positions":
      output_dir = current_config.get ("data", {}).get ("positions", {}).get ("--output_dir", default_config ["data"]["positions"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generatePositions (output_dir, pcb_file_path)

    elif cmd == "ddd":
      output_dir = current_config.get ("data", {}).get ("ddd", {}).get ("STEP", {}).get ("--output_dir", default_config ["data"]["ddd"]["STEP"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generate3D (output_dir, pcb_file_path, "STEP")

  #---------------------------------------------------------------------------------------------#

  # Process the commands with arguments or modifiers.
  for cmd in cmd_lists:
    if cmd [0] == "gerbers":
      output_dir = current_config.get ("data", {}).get ("gerbers", {}).get ("--output_dir", default_config ["data"]["gerbers"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateGerbers (output_dir, pcb_file_path)
    
    elif cmd [0] == "drills":
      output_dir = current_config.get ("data", {}).get ("drills", {}).get ("--output_dir", default_config ["data"]["drills"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateDrills (output_dir, pcb_file_path)

    elif cmd [0] == "sch_pdf":
      output_dir = current_config.get ("data", {}).get ("sch_pdf", {}).get ("--output_dir", default_config ["data"]["sch_pdf"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateSchPdf (output_dir, sch_file_path)
    
    elif cmd [0] == "bom":
      if cmd [1] == "XLS":
        pass
      else: # Default is CSV
        output_dir = current_config.get ("data", {}).get ("bom", {}).get ("CSV", {}).get ("--output_dir", default_config ["data"]["bom"]["CSV"]["--output_dir"])
        output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
        generateBom (output_dir, sch_file_path, "CSV")
    
    elif cmd [0] == "ibom":
      output_dir = current_config.get ("data", {}).get ("bom", {}).get ("iBoM", {}).get ("--output_dir", default_config ["data"]["bom"]["iBoM"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generateiBoM (output_dir, pcb_file_path)
    
    elif cmd [0] == "pcb_pdf":
      output_dir = current_config.get ("data", {}).get ("pcb_pdf", {}).get ("--output_dir", default_config ["data"]["pcb_pdf"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generatePcbPdf (output_dir, pcb_file_path)
    
    elif cmd [0] == "positions":
      output_dir = current_config.get ("data", {}).get ("positions", {}).get ("--output_dir", default_config ["data"]["positions"]["--output_dir"])
      output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
      generatePositions (output_dir, pcb_file_path)
    
    elif cmd [0] == "ddd":
      if cmd [1] == "VRML":
        output_dir = current_config.get ("data", {}).get ("ddd", {}).get ("VRML", {}).get ("--output_dir", default_config ["data"]["ddd"]["VRML"]["--output_dir"])
        output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
        generate3D (output_dir, pcb_file_path, "VRML")
        
      else: # Default is STEP
        output_dir = current_config.get ("data", {}).get ("ddd", {}).get ("STEP", {}).get ("--output_dir", default_config ["data"]["ddd"]["STEP"]["--output_dir"])
        output_dir = project_dir + "\\" + output_dir  # Output directory is relative to the project directory
        generate3D (output_dir, pcb_file_path, "STEP")
      
  return

#=============================================================================================#

def test():
  info = extract_info_from_pcb (SAMPLE_PCB_FILE)
  print (info)
  print (f"Revision is {info ['rev']}")

#=============================================================================================#

def parseArguments():
  # Configure the argument parser.
  parser = argparse.ArgumentParser (description = "KiExport: Tool to export manufacturing files from KiCad PCB projects.")
  parser.add_argument ('-v', '--version', action = 'version', version = f'{APP_VERSION}', help = "Show the version of the tool and exit.")
  subparsers = parser.add_subparsers (dest = "command", help = "Available commands.")

  # Subparser for the Run command.
  # Example: python .\kiexport.py run -if "Mitayi-Pico-D1/kiexport.json"
  run_parser = subparsers.add_parser ("run", help = "Run KiExport using the provided JSON configuration file.")
  run_parser.add_argument ("config_file", help = "Path to the JSON configuration file.")

  # Subparser for the Gerber export command.
  # Example: python .\kiexport.py gerbers -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  gerbers_parser = subparsers.add_parser ("gerbers", help = "Export Gerber files.")
  gerbers_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  gerbers_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Gerber files to.")

  # Subparser for the Drills export command.
  # Example: python .\kiexport.py drills -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  drills_parser = subparsers.add_parser ("drills", help = "Export Drill files.")
  drills_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  drills_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Drill files to.")

  # Subparser for the Position file export command.
  # Example: python .\kiexport.py positions -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  positions_parser = subparsers.add_parser ("positions", help = "Export Position files.")
  positions_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  positions_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Position files to.")

  # Subparser for the PCB PDF export command.
  # Example: python .\kiexport.py pcb_pdf -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  pcb_pdf_parser = subparsers.add_parser ("pcb_pdf", help = "Export PCB PDF files.")
  pcb_pdf_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  pcb_pdf_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the PCB PDF files to.")

  # Subparser for the Schematic PDF export command.
  # Example: python .\kiexport.py sch_pdf -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_sch"
  sch_pdf_parser = subparsers.add_parser ("sch_pdf", help = "Export schematic PDF files.")
  sch_pdf_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_sch file.")
  sch_pdf_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the Schematic PDF files to.")

  # Subparser for the 3D file export command.
  # Example: python .\kiexport.py ddd -t "VRML" -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  ddd_parser = subparsers.add_parser ("ddd", help = "Export 3D files.")
  ddd_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  ddd_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the 3D files to.")
  ddd_parser.add_argument ("-t", "--type", required = True, help = "The type of file to generate. Can be STEP or VRML.")

  # Subparser for the BoM file export command.
  # Example: python .\kiexport.py bom -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_sch"
  bom_parser = subparsers.add_parser ("bom", help = "Export BoM files.")
  bom_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_sch file.")
  bom_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the BoM files to.")
  bom_parser.add_argument ("-t", "--type", help = "The type of file to generate. Default is CSV.")

  # Subparser for the HTML iBoM file export command.
  # Example: python .\kiexport.py ibom -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
  ibom_parser = subparsers.add_parser ("ibom", help = "Export HMTL iBoM files. The Kicad iBOM plugin is required")
  ibom_parser.add_argument ("-if", "--input_filename", required = True, help = "Path to the .kicad_pcb file.")
  ibom_parser.add_argument ("-od", "--output_dir", required = True, help = "Directory to save the BoM files to.")

  # Subparser for the test function.
  test_parser = subparsers.add_parser ("test", help = "Internal test function.")

  #---------------------------------------------------------------------------------------------#

  # Parse arguments.
  args = parser.parse_args()
  printInfo()

  #---------------------------------------------------------------------------------------------#

  # Handle empty arguments.
  if args.command is None:
    print (color.red ("Looks like you forgot to specify any inputs. Time to RTFM."))
    print()
    parser.print_help()
    return
  
  #---------------------------------------------------------------------------------------------#

  # Handle the version command.
  if args.command == "-v" or args.command == "--version":
    print (f"KiExport v{APP_VERSION}")
    return

  #---------------------------------------------------------------------------------------------#

  # The Run command accepts a config file as an argument and generate the files based on the
  # config file. The name of the config file can be anything.
  if args.command == "run":
    run (args.config_file)
    return
    
  else:
    # Load the standard config file for other commands.
    if args.input_filename is not None: # Check if we received an input file
      config_file_path = os.path.join (os.path.dirname (args.input_filename), "kiexport.json")
      load_config (config_file = config_file_path)
    else:
      load_config (config_file = "kiexport.json")
  
  #---------------------------------------------------------------------------------------------#
  
  # Check the command and run it.
  
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

  elif args.command == "ibom":
    generateiBoM (args.output_dir, args.input_filename)

  elif args.command == "test":
    test()
    
  else:
    parser.print_help()

#=============================================================================================#

def printInfo():
  print ("")
  print (color.cyan (f"KiExport v{APP_VERSION}"))
  print (color.cyan ("CLI tool to export design and manufacturing files from KiCad projects."))
  print (color.cyan ("Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)"))
  print (color.cyan ("Contributors: Dominic Le Blanc (@domleblanc94)"))
  print ("")

#=============================================================================================#

def main():
  parseArguments()

#=============================================================================================#

if __name__ == "__main__":
  main()

#=============================================================================================#
