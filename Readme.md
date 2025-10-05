
# KiExport

[**KiExport**](https://github.com/vishnumaiea/KiExport) is a Python application for automating the manufacturing files generation process from KiCad PCB design projects. This is a CLI (Command Line Interface) utility. Commands and arguments can be passed to the script while running, or from a JSON configuration file named `kiexport.json`. You should be familiar working with CLI tools and how to execute commands from a terminal.

KiExport generates the manufacturing files based on the options available in the `kiexport.json` file, and saves them in an organized way. It renames the files, folders and create ZIP archive files with proper names and date stamps so that you can send them to a manufacturer or client easily. Since the `kiexport.json` configuration file can be edited for any project, you only have to create the file once. You can also create multiple configuration files according to different manufacturing requirements.

The [**Mitayi Pico RP2040**](https://github.com/CIRCUITSTATE/Mitayi-Pico-RP2040) project is added as a sample project to test the script. If you are on Windows, you can run the `EXPORT-ALL.bat` batch script to automatically generate the manufacturing files with a double-click.

- **Author:** [Vishnu Mohanan](https://github.com/vishnumaiea)
- **Version:** `0.1.10`
- **Contributors:** Dominic Le Blanc ([@domleblanc94](https://github.com/domleblanc94))

This tool was created with the help of [**ChatGPT**](https://chat.openai.com/chat). Thanks to humanity!

## Table of Contents
- [KiExport](#kiexport)
  - [Table of Contents](#table-of-contents)
  - [Why?](#why)
  - [Why not KiCad Jobsets?](#why-not-kicad-jobsets)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Example](#example)
  - [Usage](#usage)
  - [Commands](#commands)
    - [`version`](#version)
    - [`help`](#help)
    - [`pcb_drc`](#pcb_drc)
    - [`gerbers`](#gerbers)
    - [`drills`](#drills)
    - [`positions`](#positions)
    - [`pcb_pdf`](#pcb_pdf)
    - [`pcb_render`](#pcb_render)
    - [`sch_pdf`](#sch_pdf)
    - [`ddd`](#ddd)
    - [`svg`](#svg)
    - [`bom`](#bom)
    - [`run`](#run)
  - [Configuration File](#configuration-file)
  - [Log File](#log-file)
  - [License](#license)
  - [References](#references)


## Why?

- ~~Currently, exporting manufacturing files from KiCad's own UI requires setting so many options correctly and moving through different steps for different types of files.~~
- If you make a mistake in choosing the options correctly, you will end up with a "bad" manufacturing file that will waste your time later.
- ~~KiCad currently has no ability to save the export options as presets and it does not always remember the previously used options.~~
- Existing plugins available for KiCad only work for specific types of files and specific set of manufacturing options.
- The number and types of files generated from a KiCad project can be quite many. Renaming, organizing and archiving the files manually can be a tedious task. For example, we generate Gerbers, PCB PDF, Schematic PDF, STEP, VRML, CSV BoM, HTML BoM, XLS BoM, Position Files, and Preview Images for a typical project. We have to do this every time we make a change to the project to keep consistency across the set of files generated at a time.
- KiCad CLI can do almost all of what the KiCad UI can.
- Instead of typing the arguments manually to a terminal all the time, we can save the options as a JSON file and call the KiCad CLI every time we want to generate the files.

## Why not KiCad Jobsets?

KiCad V9 added support for **Jobsets** which allow you to generate manufacturing files in an automated way. However, the feature is in its early stages and causes freezes and crashes often (at least when I tried it last time). Until the feature matures enough, the development on KiExport will continue.

## Requirements

This software was developed and tested on Windows 11. It should work on other platforms as well, but it is not tested. The following software should be installed in your system to use this tool.

- [Python 3.x](https://www.python.org/downloads/)
- [KiCad 8.x or later](https://www.kicad.org/download/)
- [Git](https://git-scm.com/downloads)
- [Interactive HTML BoM Plugin](https://github.com/openscopeproject/InteractiveHtmlBom) (if you want to generate HTML BoM)
- Recommended:
  - [VS Code](https://code.visualstudio.com/download)
  - [Windows Terminal](https://github.com/microsoft/terminal/releases)

## Installation

KiExport relies on the [**KiCad-CLI**](https://docs.kicad.org/9.0/en/cli/cli.html) tool to generate the files and therefore supports all the features of KiCad-CLI. You should have a KiCad version installed in your system to use this tool. You can download and install the latest version of KiCad from [here](https://kicad.org/download/). After installation, browse to the installation folder and find the `bin` directory where the `kicad-cli.exe` file is located. Add the `bin` folder to your system `Path`. If you do not know how to add a new path to the system `Path` variable, check out any tutorials on the internet.

You can clone/fork the project to obtain a copy of the repository in your system using the following command. [Git](https://git-scm.com/downloads) should be installed and available on the path.

```bash
git clone https://github.com/vishnumaiea/KiExport.git
```

Additionally, you can download the project as a ZIP file from the main page or the [Releases](/releases) page and extract it in your system. After getting the files, you can add the project folder to the system `Path` variable. If your system opens Python script files with the Python interpreter by default, you can run any python script directly from the terminal even without using the `.py` extension as shown in the image below.

![Windows Terminal](/resources/2024-10-12_10-05-04-PM-.png)

If you are going to run the app as a Python script, install the dependencies using the following command.

```bash
pip install -r requirements.txt
```

Check if the app is working by checking the version of the tool. Open a terminal and run the following command.

```bash
kiexport -v
```

If you see the version printed, the installation is successful. Otherwise, follow the installation procedure again.

## Example

Following is a tree view of the files generated by KiExport from the **Mitayi-Pico-D1** project. A top level revision folder will be created to store the files for that specific revision. Under that, a date-specific folder will be created to store files generated in a specific day. Inside that, file-specific folders are created to store the different types of files. ZIP archives are created for some type of files that are usually sent as a set of files to the manufacturer, for example Gerbers.

If you generate the files multiple times a day, older files will be overwritten except for any files with a sequence number at the end of the filename. For example, ZIP files have a sequence number at the end of the filename after the date string. A new file with a new sequence number will be created when multiple files are generated.

```
\---R0.6
    \---2024-10-26
        +---3D
        |       Mitayi-Pico-RP2040-R0.6-STEP-26102024-1.step
        |       Mitayi-Pico-RP2040-R0.6-VRML-26102024-1.wrl
        |
        +---Position
        |       Mitayi-Pico-RP2040-R0.6-Pos-All.csv
        |       Mitayi-Pico-RP2040-R0.6-Pos-Back.csv
        |       Mitayi-Pico-RP2040-R0.6-Pos-Front.csv
        |       Mitayi-Pico-RP2040-R0.6-Position-Files-26102024-1.zip
        |
        +---BoM
        |       Mitayi-Pico-RP2040-R0.6-BoM-CSV-26102024-1.csv
        |       Mitayi-Pico-RP2040-R0.6-BoM-XLS-26102024-1.xlsx
        |       Mitayi-Pico-RP2040-R0.6-BoM-HTML-26102024-1.html
        |
        +---Gerber
        |       Mitayi-Pico-RP2040-R0.6-B_Courtyard.gbr
        |       Mitayi-Pico-RP2040-R0.6-B_Cu.gbr
        |       Mitayi-Pico-RP2040-R0.6-B_Fab.gbr
        |       Mitayi-Pico-RP2040-R0.6-B_Mask.gbr
        |       Mitayi-Pico-RP2040-R0.6-B_Paste.gbr
        |       Mitayi-Pico-RP2040-R0.6-B_Silkscreen.gbr
        |       Mitayi-Pico-RP2040-R0.6-Edge_Cuts.gbr
        |       Mitayi-Pico-RP2040-R0.6-F_Courtyard.gbr
        |       Mitayi-Pico-RP2040-R0.6-F_Cu.gbr
        |       Mitayi-Pico-RP2040-R0.6-F_Fab.gbr
        |       Mitayi-Pico-RP2040-R0.6-F_Mask.gbr
        |       Mitayi-Pico-RP2040-R0.6-F_Paste.gbr
        |       Mitayi-Pico-RP2040-R0.6-F_Silkscreen.gbr
        |       Mitayi-Pico-RP2040-R0.6-Gerber-26102024-1.zip
        |       Mitayi-Pico-RP2040-R0.6-job.gbrjob
        |       Mitayi-Pico-RP2040-R0.6-NPTH-drl_map.pdf
        |       Mitayi-Pico-RP2040-R0.6-NPTH.drl
        |       Mitayi-Pico-RP2040-R0.6-PTH-drl_map.pdf
        |       Mitayi-Pico-RP2040-R0.6-PTH.drl
        |       Mitayi-Pico-RP2040-R0.6-User_Comments.gbr
        |       Mitayi-Pico-RP2040-R0.6-User_Drawings.gbr
        |
        +---PCB
        |       Mitayi-Pico-RP2040-R0.6-B_Courtyard.pdf
        |       Mitayi-Pico-RP2040-R0.6-B_Cu.pdf
        |       Mitayi-Pico-RP2040-R0.6-B_Fab.pdf
        |       Mitayi-Pico-RP2040-R0.6-B_Mask.pdf
        |       Mitayi-Pico-RP2040-R0.6-B_Paste.pdf
        |       Mitayi-Pico-RP2040-R0.6-B_Silkscreen.pdf
        |       Mitayi-Pico-RP2040-R0.6-Edge_Cuts.pdf
        |       Mitayi-Pico-RP2040-R0.6-F_Courtyard.pdf
        |       Mitayi-Pico-RP2040-R0.6-F_Cu.pdf
        |       Mitayi-Pico-RP2040-R0.6-F_Fab.pdf
        |       Mitayi-Pico-RP2040-R0.6-F_Mask.pdf
        |       Mitayi-Pico-RP2040-R0.6-F_Paste.pdf
        |       Mitayi-Pico-RP2040-R0.6-F_Silkscreen.pdf
        |       Mitayi-Pico-RP2040-R0.6-PCB-PDF-26102024-1.zip
        |       Mitayi-Pico-RP2040-R0.6-PCB-PDF-All-26102024-1.pdf
        |       Mitayi-Pico-RP2040-R0.6-User_Comments.pdf
        |       Mitayi-Pico-RP2040-R0.6-User_Drawings.pdf
        |
        +---Render
        |       Mitayi-Pico-RP2040-R0.6-Top-26102024-1.png
        |       Mitayi-Pico-RP2040-R0.6-Bottom-26102024-1.png
        |       Mitayi-Pico-RP2040-R0.6-Front-26102024-1.png
        |       Mitayi-Pico-RP2040-R0.6-Back-26102024-1.png
        |
        +---Report
        |       Mitayi-Pico-RP2040-R0.6-DRC-26102024-1.rpt
        |       Mitayi-Pico-RP2040-R0.6-DRC-26102024-1.json
        |
        +---SCH
        |       Mitayi-Pico-RP2040-R0.6-SCH-26102024-1.pdf
        |
        \---SVG
                Mitayi-Pico-RP2040-R0.6-SVG-26102024-1.svg
```

## Usage

You can run the Python script directly from the source folder with the following command. Python should be installed and available on the `Path`.

```bash
python kiexport.py <command> <arguments>
```

In addition, you can also run the Windows executable `kiexport.exe` with the following command. The `dist` folder should be added to the system `Path` in order for this to work.

```bash
kiexport <command> <arguments>
```

You can automate running multiple commands with a batch script if you are on Windows. Refer to the [`EXPORT-ALL.bat`](/Mitayi-Pico-D1/EXPORT-ALL.bat) file for an example. Run the script to see KiExport in action.

```bat
@REM @echo off

:: Set variables
set OUTPUT_DIR=Export
set SCH_FILE=Mitayi-Pico-RP2040.kicad_sch
set PCB_FILE=Mitayi-Pico-RP2040.kicad_pcb

:: Execute commands
@REM kiexport pcb_drc -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "report"
@REM kiexport sch_pdf -od "%OUTPUT_DIR%" -if "%SCH_FILE%"
@REM kiexport bom -od "%OUTPUT_DIR%" -if "%SCH_FILE%" -t "CSV"
@REM kiexport bom -od "%OUTPUT_DIR%" -if "%SCH_FILE%" -t "XLS"
@REM kiexport bom -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "HTML"
@REM kiexport pcb_pdf -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport pcb_render -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport gerbers -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport positions -od "%OUTPUT_DIR%" -if "%PCB_FILE%"
@REM kiexport ddd -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "STEP"
@REM kiexport ddd -od "%OUTPUT_DIR%" -if "%PCB_FILE%" -t "VRML"

pause
```

You can also create a batch file for running the `run` command as shown below. You can then double-click on the script every time you want to generate new files, saving you from typing the same commands over and over.

```bash
kiexport run Mitayi-Pico-D1/kiexport.json

pause
```

## Commands

### `version`

Run the following command to show the version of the tool.

```bash
kiexport -v
```

```bash
kiexport --version
```

### `help`

Show the help menu.

```bash
kiexport -h
```

```bash
kiexport --help
```

You can include the command to get the help menu of a specific command. For example,

```bash
kiexport gerbers -h
```

### `pcb_drc`

Runs a DRC (Design Rule Check) on the PCB file. If there are errors in the design, evaluated as per the DRC rules, the command will return the type and number of errors found. It will also generate a report file and save it to the output directory. When ran as part of the `run` command, you can choose to skip other commands if there are DRC errors. The configruation for this command can be specified in the configuration file under the `pcb_drc` section. If a format type is specified in the CLI command, it will override the type specified in the configuration file.

```bash
kiexport pcb_drc -if <input_file> -od <output_dir> -t <type>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory where the report will be saved. Required.
- `-t`: The type of report to generate. Possible values are `report`, and `json`. Optional. Defaults to the type specified in the configuration file.
  - `report` - Generates a text report file with `.rpt` extension.
  - `json` - Generates a JSON report file with `.json` extension.

### `gerbers`

Export the Gerber files. Gerber files export does not include the drill files by default. If you want to generate the drill files as well, you can either manually run the `drills` command or enable the drill file generation in the JSON configuration file using the `kie_include_drill` flag.

```bash
kiexport gerbers -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport gerbers -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export"
```

### `drills`

Generate the drill files. If you are generating drill files along with the `gerbers` command, you don't need to run this command again. Otherwise, the drill files will be generated twice.

```bash
kiexport drills -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport drills -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export"
```

### `positions`

Export the Position or Centroid files for PCB assembly (PCBA).

```bash
kiexport positions -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport positions -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export"
```

### `pcb_pdf`

Export the PCB layers as individual PDF.

```bash
kiexport pcb_pdf -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport pcb_pdf -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export"
```

### `pcb_render`

Export the PCB as a rendered image.

```bash
kiexport pcb_render -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport pcb_render -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export"
```

### `sch_pdf`

Export the schematic as PDF.

```bash
kiexport sch_pdf -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_sch` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport sch_pdf -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_sch" -od "Mitayi-Pico-D1/Export"
```

### `ddd`

Export the 3D files. Generating STEP files can take some time when the PCB is large. Wait for the process to complete. VRML file generation is faster.

```bash
kiexport ddd -if <input_file> -od <output_dir> -t <type>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.
- `-t`: The type of 3D file to export. Possible values are `STEP` and `VRML`. Required.

Example:

```bash
kiexport ddd -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export" -t STEP
```

### `svg`

Export the PCB as SVG files. The list of layers can be specified in the config file. You can also define common layers to be used when generating each layer. A ZIP file is created at the end while keeping the original files intact. Each run of the command will overwrite the standalone files but will create a new ZIP file with a new sequence number.

```bash
kiexport svg -if <input_file> -od <output_dir>
```

- `-if`: Path to the input `.kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.

Example:

```bash
kiexport svg -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb" -od "Mitayi-Pico-D1/Export"
```

### `bom`

Export the bill of materials files.

```bash
kiexport bom -if <input_file> -od <output_dir> -t <type>
```

- `-if`: Path to the input `.kicad_sch`/`kicad_pcb` file. Required.
- `-od`: Path to the output directory. Required.
- `-t`: The type of bill of materials to export. Possible values are `CSV`, `XLS`, and `HTML`. Optional. Defaults to `CSV`.
  - `CSV` & `XLS` - Requires `.kicad_sch` file.
  - `HTML` - Requires `.kicad_pcb` file.

Example:

```bash
kiexport bom -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_sch" -od "Mitayi-Pico-D1/Export" -t CSV
```

Exporting the HTML BoM requires the [Interactive HTML BoM](https://github.com/openscopeproject/InteractiveHtmlBom) plugin for KiCad. The plugin should be available in your PC. You need to add the paths to the `generate_interactive_bom.py` script and the KiCad Python (`"C:\Program Files\KiCad\8.0\bin\python.exe"` for example) to the JSON configuration file. Check the configuration file available in the `Mitayi-Pico-D1` folder for an example.

Example:

```bash
kiexport ibom -od "Mitayi-Pico-D1/Export" -if "Mitayi-Pico-D1/Mitayi-Pico-RP2040.kicad_pcb"
```

### `run`

This command can be used to generate multiple types of files by providing just a valid JSON configuration file. Unlike other commands which will look specifically for the `kiexport.json` file, this command will accept a JSON file with any name. This is useful when you need different configurations for different manufacturers and use-cases. You can create a configuration file for each manufacturer and use them with the `run` command individually. Check out the [`kiexport.json`](Mitayi-Pico-D1/kiexport.json) file for an example configuration file.

Since the `run` command does not accept any configuration parameters directly, everything needed to generate the manufacturing files should be in the JSON configuration file. Additionally, `run` can also accept a subset of commands to run from the supplied configuration file. This can be useful when you do not want to run the commands individually.

```bash
kiexport run <config_file> <commands>
```

- `<config_file>`: Path to the JSON configuration file. Required.
- `<commands>`: A list of commands to run from the configuration file. Optional. The list of commands should be a comma separated string in the same format as the `commands` key in the configuration file. Do not use quotes for individual commands in this case.

Example:

```bash
kiexport run Mitayi-Pico-D1/kiexport.json

kiexport run Mitayi-Pico-D1/kiexport.json "gerbers, positions"
kiexport run Mitayi-Pico-D1/kiexport.json "pcb_pdf, sch_pdf"
kiexport run Mitayi-Pico-D1/kiexport.json "gerbers, [ddd, STEP], [ddd, VRML]"
```

## Configuration File

KiExport supports a JSON configuration file called `kiexport.json`. The name of the file should be exact when running the all of the generic commands except `run`. The `run` command will accept a configuration file with any name. The configuration file should be placed in the root folder of your KiCad project where the main `.kicad_sch` and `.kicad_pcb` files are located. Check the `Mitayi-Pico-D1` folder for an example. A copy of the default configuration file is integrated into the script to use as the default one. So if any of the input parameters are missing from your configuration file, the script will use the default values.

To create a configuration file for your own project, add the `project_name`, the required commands under `commands`. The commands can be a simple list of strings, or a nested list. You can add any number of instances of the same command. The data for the commands should be added under `data`.  All keys that starts with `--` are directly passed to the KiCad-CLI and anything that starts with `kie_` is a data for the KiExport application.

If you want to disable any of the commands in the `commands` list, you can simply prefix or suffix them with, for example `_`, and KiExport will ignore such invalid commands. This is better than deleting the commands.

## Log File

KiExport will generate a log file in a directory specified in the configuration file. This log can be used to check what commands were run and what files were created in the last run. The log file can be specified in the configuration file as follows for example:

```json
"kiexport_log_path": "Export\\kiexport.log"
```

## License

This project is licensed under the MIT license.

## References

- [KiCad Command-Line Interface](https://docs.kicad.org/9.0/en/cli/cli.html)
- [Getting Started with KiCad Version 6 : Beginner’s Tutorial to Schematic and PCB Design](https://www.circuitstate.com/tutorials/getting-started-with-kicad-version-6-beginners-tutorial-to-schematic-and-pcb-design/)
- [How to Install KiCad Version 6 and Organize Part Libraries](https://www.circuitstate.com/tutorials/how-to-install-kicad-version-6-and-organize-part-libraries/)
- [How to Get Your KiCad PCB Design Ready for Automated Assembly – KiCad 6 Tutorial](https://www.circuitstate.com/tutorials/how-to-get-your-kicad-pcb-design-ready-for-automated-assembly-kicad-6-tutorial/)
- [How to Get Your KiCad PCB Design Ready for Fabrication – KiCad Version 6 Tutorial](https://www.circuitstate.com/tutorials/how-to-get-your-kicad-pcb-design-ready-for-fabrication-kicad-version-6-tutorial/)
- [Interactive HTML BoM for KiCad](https://github.com/openscopeproject/InteractiveHtmlBom)

