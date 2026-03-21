@REM @echo off

:: Set variables
set OUTPUT_DIR=Export
set SCH_FILE=Mitayi-Pico-D1.kicad_sch
set PCB_FILE=Mitayi-Pico-D1.kicad_pcb

:: Execute commands
@REM kiexport sch_pdf -od "%OUTPUT_DIR%" -if "%SCH_FILE%"
@REM kiexport bom -od "%OUTPUT_DIR%" -if "%SCH_FILE%" -t "CSV"
@REM kiexport bom -od "%OUTPUT_DIR%" -if "%SCH_FILE%" -t "XLS"
@REM kiexport bom -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "HTML"
@REM kiexport pcb_pdf -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport pcb_svg -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport pcb_render -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport gerbers -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport positions -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport ddd -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "STEP"
@REM kiexport ddd -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "VRML"
@REM kiexport ddd -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "3DPDF"

kiexport run "kiexport.json"

pause
