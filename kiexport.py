
#=============================================================================================#

# KiExport
# Tool to export manufacturing files from KiCad PCB projects.
# Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)
# Version: 0.0.2
# Last Modified: +05:30 23:19:21 PM 29-08-2024, Thursday
# GitHub: https://github.com/vishnumaiea/KiExport
# License: MIT

#=============================================================================================#

import subprocess
import argparse

#=============================================================================================#

def generateGerbers (output_dir, pcb_filename):
  # Common base command
  gerber_export_command = ["kicad-cli", "pcb", "export", "gerbers"]

  # Assemble the full command for Gerber export
  # output_dir = "Mitayi-Pico-D1/Gerber"
  layer_list = "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,User.Drawings,User.Comments,Edge.Cuts,F.Courtyard,B.Courtyard,F.Fab,B.Fab"
  # pcb_filename = "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"

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
