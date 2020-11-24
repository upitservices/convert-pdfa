try:
    from PIL import Image
except ImportError:
    import Image

import subprocess
import datetime
import os
import re
import json
import sys
from pathlib import Path
import pytesseract

gs_executable = None
tesseract_executable = None
source_dir = None
destination_dir = None
destination_dir_img = None
tiff_files = []

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
conf_path = os.path.join(current_directory, "conf.json")

with open(conf_path, encoding='utf-8') as json_file:
    data = json.load(json_file)
    source_dir = Path(data['source_dir'])
    destination_dir = Path(data['destination_dir'])
    destination_dir_img = Path(data['destination_dir_img'])
    gs_executable = r"{}".format(data['gs_executable'])
    tesseract_executable = r"{}".format(data['tesseract_executable'])

if not data or not source_dir or not destination_dir or not gs_executable:
    print('Missing config parameters')
    exit()

# Ghostscript command to convert pdf into tiff files so we can process them on Tesseract
gs_command = [gs_executable,  '-dBATCH', '-dNOPAUSE', '-sDEVICE=tiff24nc', '-r300']
pytesseract.pytesseract.tesseract_cmd = tesseract_executable

def convert(file_src_path, dest_path):
    cwd = os.getcwd()
    os.chdir(os.path.dirname(dest_path))
    try:
        subprocess.check_output(gs_command + ['-sOutputFile="' + dest_path + '"', file_src_path])
        # os.remove(file_src_path)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("'{}' returned the following error: (code {}): {}".format(e.cmd, e.returncode, e.output))

    os.chdir(cwd)

if not sys.argv[1]:
    for dirname, subdirs, files in os.walk(source_dir):
        for file in [f for f in files if f.upper().endswith("PDF")]:
            full_path = os.path.join(dirname, file)
            full_dest_path = os.path.join(destination_dir_img, os.path.basename(full_path))
            full_dest_path = re.sub(r'(\.pdf)', r'.tif', full_dest_path).lower()
            convert(full_path, full_dest_path)
else:
    full_path = sys.argv[1]
    full_dest_path = os.path.join(destination_dir_img, os.path.basename(full_path))
    full_dest_path = re.sub(r'(\.pdf)', r'.tif', full_dest_path).lower()
    convert(full_path, full_dest_path)

# Getting the list of all files and converting them to PDF with OCR with tesseract
for dirname, subdirs, files in os.walk(destination_dir_img):
    for file in [f for f in files if f.upper()]:
        full_path = os.path.join(dirname, file)
        tiff_files.append(full_path)

str_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
resulting_pdf = "result-{}.pdf".format(str_datetime)
pdf = pytesseract.image_to_pdf_or_hocr(''.join(tiff_files), extension='pdf')
with open(os.path.join(destination_dir, resulting_pdf), 'w+b') as f:
    f.write(pdf)

# Removing tiff source files
for image_path in tiff_files:
    os.remove(image_path)