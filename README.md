# PDF to PDF/A + OCR Converter

Simple python script to convert all PDF files from a source folder into PDF/A + OCR
using GhostScript.

## Installation

You'll need to install [ghostscript](https://www.ghostscript.com/), [tesseract](https://github.com/tesseract-ocr/tesseract) and python3 to run this script. For now,


### If you're using Ubuntu, just use apt

`sudo apt install python3 ghostscript tesseract-ocr`

After installing python and GS and Tesseract, clone this repository wherever you want and install the dependencies on your environment using pip:

`pip install -r requirements.txt`

This script was under Ubuntu environment and Windows 10/Server

If your Python installation has Tk, just execute `python config.py`, set the
fields to the paths for your GS, tesseract, source and destination folder and your're done.
The tool will create the conf.json file for you.

If you just want to set the json file manually, rename the *conf.json.example* 
to *conf.json*. There will be the following parameters to be set:

- gs_executable: The path for your Ghostscript installation. (If it is in the system path, just put the name of the command, e.g: gs)
- tesseract_executable: The path for your Tesseract installation.
- source_dir: The full path for the source PDF files
- destination_dir: The full path where you want the final PDF/A files.
- destination_dir_img: The full path where the script will generate the temp tiff image files (they'll be deleted after OCR process)
- destination_dir_ocr: The full path where the searchable PDF will be generated before the PDF/A conversion process

**Warning**: Your source files will be deleted after the convertion, even though the convertion was not sucessfull, so be careful when using this script, since we don't take any responsibility for lost data or anything you do with it. (But we would be grateful if someone could improve it)

### Usage

```
usage: convert.py [-h] [--file FILE] [--ocr OCR]
                  [--keep_filename KEEP_FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           PDF file to be converted
  --ocr OCR             true to make the PDF searchable before converting to
                        PDF/A
  --keep_filename KEEP_FILENAME
                        true to keep the original filename after conversion
```

## Licence

This script is licensed as Apache Software License 2.0, but since it 
uses Ghostscript, might be under it's own license.

Use this script at your own risk for any purpose. 