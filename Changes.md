

#
### **+05:30 11:12:50 PM 13-02-2025, Thursday**

  - Added common layers support for SVG generation.
    - New `kie_common_layers` parameter under SVG configuration.
  - SVG files are now saved as ZIP file.

#
### **+05:30 07:35:29 PM 18-12-2024, Wednesday**

  - Fixed crashing when opening a source file without specifying the encoding.

#
### **+05:30 09:55:52 PM 11-11-2024, Monday**

  - Fixed app exiting when either `kicad_python_path` or `ibom_path` are not found.
    - The `generateiBoM()` will now skip the command if either of the paths are not found.
  - Fixed whitespace handling in paths in `generateiBoM()` function.

#
### **+05:30 06:07:24 PM 09-11-2024, Saturday**

  - Updated Readme.
    - Added `svg` command documentation.

#
### **+05:30 11:54:14 PM 08-11-2024, Friday**

  - Added SVG generation support.
    - Added `generateSvg()` function.
    - Added `svg` command.
    - Updated the JSON with SVG generation options.
    - Tested and working.
  - New Version `0.0.27`.

#
### **+05:30 11:02:36 PM 08-11-2024, Friday**

  - Fixed the `rename_files()` not handling an empty extension list.
    - It will now rename all files when the extension list is empty.
    - Thanks to `@domleblanc94`.
  - Added docstring to `rename_files()` function.

#
### **+05:30 07:27:45 PM 08-11-2024, Friday**

  - Removed unused libraries.
  - Fixed the issue of the app exiting when trying to generate files from PCB-only projects that do not have a schematic file in the project folder.
    - The app will now warn about the missing files (either schematic of PCB) and will skip the commands that require the missing files.

#
### **+05:30 09:56:10 PM 05-11-2024, Tuesday**

  - Fixed fstring quotes mismatches.

#
### **+05:30 08:22:02 PM 04-11-2024, Monday**

  - Updated Readme.
    - Added `run` command documentation.
    - Updated Configuration File documentation.

#
### **+05:30 08:04:52 PM 04-11-2024, Monday**

  - Exported EXE for version `0.0.26`.

#
### **+05:30 10:29:54 PM 03-11-2024, Sunday**

  - Updated the JSON configuration file version to `1.2`.
  - Updated the default configuration.
  - Updated the way all of the functions read and interpret the output directories.
    - Output directories are now relative to the project path.
    - Absolute paths will be used always to avoid any problems.
  - Updated `create_final_directory()` function.
    - The CLI argument `--output_dir` has now precedence over what is in the JSON configuration file.
  - Added default type of "STEP" to `generate3D()` function.
  - Updated `run()`.
    - It can now generate the complete set of files using the info from the JSON configuration file.
    - The directory of the configuration file should be the same as the project path.
  - Tested and working correctly.

#
### **+05:30 02:49:52 PM 03-11-2024, Sunday**

  - Added documentation to `load_config()`.
  - Added **# TODO:** Check the JSON configuration file version and warn about consequences.

#
### **+05:30 02:38:19 PM 03-11-2024, Sunday**

  - Simplified `load_config()`.
    - Removed the extra `project_file` argument.
    - Now the configuration can be loaded as a relative or absolute path.
    - The default configuration file name will still be `kiexport.json`.
  - Added new `run` command and `run()` function.
    - This will generate files based on the provided JSON configuration file.
    - The configuration file can be anything.
  - New Version `0.0.26`

#
### **+05:30 08:16:16 PM 02-11-2024, Saturday**

  - Updated Readme
    - Updated documentation.
    - Updated contributors list.

#
### **+05:30 07:33:18 PM 02-11-2024, Saturday**

  - Updated `generateiBoM()`
    - `kicad_python_path` and `ibom_path` variables are now loaded from the `kiexport.json` file.
    - Bothe paths are now checked for existence.
  - Bumped up the `kiexport.json` JSON version to `1.1`.
  - Updated the default configuration.

#
### **+05:30 06:58:52 PM 02-11-2024, Saturday**

  - Updated `generateiBoM()`
    - The function now follows the same procedure as all other functions.
    - Output directory is now created if it does not exist.
    - The `kicad_python_path` and the `ibom_path` variables are now hardcoded. These need to be made configurable in the future.
    - Custom file name is created based on the sequence number.
    - Added complete set of Interactive HTML BoM plugin command list to the `kiexport.json` file, with most of the default options.
    - Arguments are now fetched and passed automatically to the `generate_interactive_bom.py` script.
    - The `--output-dir` command will be used instead of native `--dest-dir` command.
    - Tested and working correctly.
  - New Version `0.0.25`.

#
### **+05:30 04:10:26 PM 02-11-2024, Saturday**

  - Renamed `run_kicad_ibom()` to `generateiBoM()`.

#
### **+05:30 01:23:57 PM 02-11-2024, Saturday**

  - Updated `merge_pdfs()`
    - Fixed indentation issues.
    - Fixed styling.
    - Updated debug message formats.
    - Disabled (commented out) deleting of original PDF files after merging.
    - Tested and working correctly.
  - Updated `generatePcbPdf()`
    - Now creates a merged PDF file along with the individual PDF files.
    - Updated the merged PDF file's name format.
    - Enabled generating ZIP file with the merged PDF files.
    - Tested and working correctly.
  - New Version `0.0.24`.

#
### **+05:30 08:27:56 PM 19-10-2024, Saturday**

  - Created executable for version `0.0.23`.
  - Updated Readme.

#
### **+05:30 10:12:46 PM 15-10-2024, Tuesday**

  - PCB PDF files are now saved as ZIP file also.
  - New Version `0.0.23`.

#
### **+05:30 09:49:11 PM 12-10-2024, Saturday**

  - Changed the final directory date format to `"YYYY-MM-DD"` from `"DD-MM-YYYY"`. This will help the directories to be sorted easily by name by default.
  - New Version `0.0.22`.

#
### **+05:30 11:47:28 PM 07-10-2024, Monday**

  - Added colors to the directory name strings in the `create_final_directory()` function.

#
### **+05:30 08:23:25 PM 07-10-2024, Monday**

  - Fixed string quotes conflicts.
  - New Version `0.0.21`.

#
### **+05:30 05:08:48 PM 06-10-2024, Sunday**

  - Added JSON configuration support for `generateBom()`.
  - New Version `0.0.20`.

#
### **+05:30 04:46:12 PM 06-10-2024, Sunday**

  - Added JSON configuration support for `generate3D()`.
  - New Version `0.0.19`.

#
### **+05:30 03:33:44 PM 06-10-2024, Sunday**

  - Optimized the `generatePositions()` function.
  - New Version `0.0.18`.

#
### **+05:30 01:39:08 AM 06-10-2024, Sunday**

  - Added support JSON configuration for `generatePcbPdf()`.
  - Added color to the printed app info.
  - New Version `0.0.17`.

#
### **+05:30 12:26:25 AM 07-09-2024, Saturday**

  - `generateGerbers()` now reads the configuration `kie_include_drill` and generated the drill files first based on the value. Default value is `true`.
  - New Version `0.0.16`.

#
### **+05:30 12:02:33 AM 07-09-2024, Saturday**

  - Bumped up the version to `0.0.15`.

#
### **+05:30 11:50:10 PM 06-09-2024, Friday**

  - So many changes.
  - Added `Colorize` and `_color` classes and `color` object to colorize text in the terminal.
  - Added text colors in multiple places for error messages, file names and commands.
  - `generateGerbers()` can now completely read the configuration from the `kiexport.json` file.
  - Added `delete_files()` function to delete files with the specified extensions, with inclusion and exclusion options.
  - Added `rename_files()` to rename files in a folder. It accepts the file extensions as a list.
  - Replaced `zip_all_files()` with `zip_all_files_2()`. The latter can now accept a list of file extensions to include in the zip file.
  - Updated `generateDrills()` as a standalone generator.
    - It saves the files to the same `Gerber` directory.
    - It does not create a ZIP file.
    - It can use the JSON configuration file.
  - Added `drills` command to generate drill files.
  - The app will now print help message when called without any arguments.

#
### **+05:30 12:00:51 AM 05-09-2024, Thursday**

  - Updated `generatePositions()` to use the JSON configuration file.
  - File generation is successful.
  - New Version `0.0.14`.

#
### **+05:30 12:23:41 AM 04-09-2024, Wednesday**

  - Added `create_final_directory()` to create target directories.

#
### **+05:30 12:10:32 AM 03-09-2024, Tuesday**

  - Replaced the `--output` argument from the configuration list with `--output_dir`. Since we already uses revision/date/sequence based output directories, it doesn't make sense to get `--output` value for the KiCad-CLI.
  - The new `--output_dir` will be used as the root directory for the output files.

#
### **+05:30 11:52:42 PM 02-09-2024, Monday**

  - Added full support for reading `sch_pdf` command related arguments from the config file.

#
### **+05:30 10:20:21 PM 02-09-2024, Monday**

  - Added support for local JSON configuration file.
  - Updated `generateSchPdf()` to use output directory from the config file.
  - Added `load_config()` to load the custom and default configurations.
  - New Version `0.0.13`.

#
### **+05:30 12:41:33 PM 01-09-2024, Sunday**

  - Added `export.bat` script.
  - Updated Readme.
    - Added the export batch file usage.

#
### **+05:30 11:45:20 AM 01-09-2024, Sunday**

  - Added `printInfo()` to print the app information.
  - Added `-v` and `--version` command to print the app version.
  - New Version `0.0.12`.

#
### **+05:30 11:16:59 AM 01-09-2024, Sunday**

  - Added `bom` command to export BoM file. Only CSV is supported at the moment.
  - Added `generateBom()` function.
  - New Version `0.0.11`.

#
### **+05:30 10:38:08 AM 01-09-2024, Sunday**

  - Added `sch_pdf` export command. This will export the schematic as a single PDF.
  - Added `generateSchPdf()` function.
  - Schematic PDF generation is successful.

#
### **+05:30 12:16:46 AM 31-08-2024, Saturday**

  - Added `ddd` command to export STEP and VRML files.
  - Added `generate3D()` function.
  - New Version `0.0.10`.

#
### **+05:30 11:10:42 PM 30-08-2024, Friday**

  - Added `generatePcbPdf()` to export the PCB as PDF files. Layers are imported in individual files with the `Edge.Cuts` as the common layer.
  - Added `pcb_pdf` command.
  - New Version `0.0.9`.

#
### **+05:30 10:40:59 PM 30-08-2024, Friday**

  - Added `generatePositions()` to export position/centroid files.
  - Added new command `positions`.
  - New Version `0.0.8`.

#
### **+05:30 09:38:10 PM 30-08-2024, Friday**

  - Added `generateDrills()`.
  - Drill files are now generated with the Gerbers.
  - All files in the Gerber target directory, except ZIP files are now deleted before overwriting. This fixes the rename conflicts.
  - If a ZIP file already exists, the new one will now get a new sequence number. This will keep single set of manufacturing files but multiple ZIP files.
  - New Version `0.0.7`.

#
### **+05:30 02:09:09 AM 30-08-2024, Friday**

  - Generated Gerber files are now renamed with the revision tag after the project name.
  - Gerber files are now compressed into a ZIP file using `zip_all_files()`.
  - New Version `0.0.6`.

#
### **+05:30 12:17:50 AM 30-08-2024, Friday**

  - Added `extract_info_from_pcb()` to extract project information from the KiCad PCB file.
  - Now creates Gerber output directory from project revision, current date and a sequence number.
  - `to_overwrite` in `generateGerbers()` function now controls whether or not to overwrite the existing Gerber files in the target directory.
  - Added `test` command and `test()` function.
  - New Version `0.0.5`.
  
#
### **+05:30 11:39:24 PM 29-08-2024, Thursday**

  - Output directory is now created if it does not exist, in `generateGerbers()` function.
  - KiCad-CLI commands will fail if the output directory does not exist.
  - New Version `0.0.4`.

#
### **+05:30 11:33:55 PM 29-08-2024, Thursday**

  - Added `check_file_exists()` to check is a file exists.
  - Added `extract_project_name()` to extract the project name from the file name. This simply removes the extension.
  - Added `extract_pcb_file_name()` to extract the file name from the path.
  - `generateGerbers()` now prints the KiCad PCB project name.
  - Code running successfully.
  - New Version `0.0.3`.

#
### **+05:30 11:18:09 PM 29-08-2024, Thursday**

  - Added CLI argument parser.
  - Added `parseArguments()`.
  - Added `gerbers` command to export Gerber files.
  - `generateGerbers()` function now accepts the input PCB file name and the output directory path.
  - New Version `0.0.2`.

#
### **+05:30 10:45:47 PM 29-08-2024, Thursday**

  - Gerber files exported successfully.
  - Added `generateGerbers()` function.
  - Added Readme and Changes.
  - Added project info.
  - New Version `0.0.1`.
