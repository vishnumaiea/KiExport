@REM @echo off

:: Set variables
set OUTPUT_DIR=Export
set SCH_FILE=Mitayi-Pico-RP2040.kicad_sch
set PCB_FILE=Mitayi-Pico-RP2040.kicad_pcb

:: Execute commands
kiexport sch_pdf -od "%OUTPUT_DIR%" -if "%SCH_FILE%"
kiexport bom -od "%OUTPUT_DIR%" -if "%SCH_FILE%"
kiexport pcb_pdf -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
kiexport gerbers -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
kiexport positions -od "%OUTPUT_DIR%" -if "%PCB_FILE%"

pause
