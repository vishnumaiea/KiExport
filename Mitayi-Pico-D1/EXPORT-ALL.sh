#!/bin/bash

# 1. Force the shell to read aliases inside scripts
shopt -s expand_aliases 2>/dev/null || set -o aliases

# 2. Source your profile to load the 'kiexport' alias
source ~/.zshrc

# Set variables
OUTPUT_DIR="Export"
SCH_FILE="Mitayi-Pico-D1.kicad_sch"
PCB_FILE="Mitayi-Pico-D1.kicad_pcb"

# Execute commands
# kiexport sch_pdf -od "$OUTPUT_DIR" -if "$SCH_FILE"
# kiexport bom -od "$OUTPUT_DIR" -if "$SCH_FILE" -t "CSV"
# kiexport bom -od "$OUTPUT_DIR" -if "$SCH_FILE" -t "XLS"
# kiexport bom -od "$OUTPUT_DIR" -if "$PCB_FILE" -t "HTML"
# kiexport pcb_pdf -od "$OUTPUT_DIR" -if "$PCB_FILE"
# kiexport pcb_svg -od "$OUTPUT_DIR" -if "$PCB_FILE"
# kiexport pcb_render -od "$OUTPUT_DIR" -if "$PCB_FILE"
# kiexport gerbers -od "$OUTPUT_DIR" -if "$PCB_FILE"
# kiexport positions -od "$OUTPUT_DIR" -if "$PCB_FILE"
# kiexport ddd -od "$OUTPUT_DIR" -if "$PCB_FILE" -t "STEP"
# kiexport ddd -od "$OUTPUT_DIR" -if "$PCB_FILE" -t "VRML"
# kiexport ddd -od "$OUTPUT_DIR" -if "$PCB_FILE" -t "3DPDF"

# Run the active command using your global alias shortcut
# kiexport run "kiexport-mac.json" "[bom, HTML]"
kiexport run "kiexport-mac.json"

# Pause script (macOS equivalent of windows "pause")
read -p "Press [Enter] key to continue..."
