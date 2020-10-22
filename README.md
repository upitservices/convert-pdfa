# PDF to PDF/A Converter

Simple python script to convert all PDF files from a source folder into PDF/A
using GhostScript.

## Installation

You'll need to install ghostscript, and python3 to run this script. For now,
just tested under Ubuntu environment, but since Windows does have versions for
these dependencies, I think you'll be able to install them under Microsoft OS.

### For Ubuntu, just use apt

`sudo apt install python3 ghostscript`

After installing python and GS, clone this repository wherever you want and
rename the file *conf.json.example* to *conf.json*. There will be 3 parameters
to be set:

- gs_executable: The path for your Ghostscript installation. (If it is in the system path, just put the name of the command, e.g: gs)
- source_dir: The full path for the source PDF files
- destination_dir: The full path where you want the final PDF/A files.

**Warning**: Your source files will be deleted after the convertion, even though the convertion was not sucessfull, so be careful when using this script, since we don't take any responsibility for lost data or anything you do with it. (But we would be grateful if someone could improve it)

## Licence

This script is licensed as Apache Software License 2.0, but since it 
uses Ghostscript, might be under it's own license.

Use this script at your own risk for any purpose. 