
#=============================================================================================#

# KiExport
# Tool to export manufacturing files from KiCad PCB projects.
# Author: Vishnu Mohanan (@vishnumaiea, @vizmohanan)
# Version: 0.0.1
# Last Modified: +05:30 23:04:32 PM 29-08-2024, Thursday
# GitHub: https://github.com/vishnumaiea/KiExport
# License: MIT

#=============================================================================================#

import subprocess

#=============================================================================================#

def generateGerbers():
  # Common base command
  gerber_export_command = ["kicad-cli", "pcb", "export", "gerbers"]

  # Assemble the full command for Gerber export
  output_dir = "Mitayi-Pico-D1/Gerber"
  layer_list = "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,User.Drawings,User.Comments,Edge.Cuts,F.Courtyard,B.Courtyard,F.Fab,B.Fab"
  input_file_name = "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"

  full_command = gerber_export_command + \
                ["--output", output_dir] + \
                ["--no-protel-ext"] + \
                ["--layers", layer_list] + \
                ["--no-netlist"] + \
                ["--use-drill-file-origin"] + \
                [input_file_name]
  
  # Run the command
  try:
    subprocess.run (full_command, check = True)
    print ("Gerber files exported successfully.")
  except subprocess.CalledProcessError as e:
    print (f"Error occurred: {e}")

#=============================================================================================#

def main():
  generateGerbers()

#=============================================================================================#

if __name__ == "__main__":
  generateGerbers()

#=============================================================================================#
