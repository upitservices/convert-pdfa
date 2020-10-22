import subprocess
import os
import json
from pathlib import Path

gs_executable = None
source_dir = None
destination_dir = None

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
conf_path = os.path.join(current_directory, "conf.json")

with open(conf_path, encoding='utf-8') as json_file:
    data = json.load(json_file)
    source_dir = Path(data['source_dir'])
    destination_dir = Path(data['destination_dir'])
    gs_executable = r"{}".format(data['gs_executable'])

if not data or not source_dir or not destination_dir or not gs_executable:
    print('Missing config parameters')
    exit()

gs_command = [gs_executable, '-dPDFA', '-dBATCH', '-dNOPAUSE', 
                   '-sColorConversionStrategy=UseDeviceIndependentColor',
                   '-sDEVICE=pdfwrite', '-dPDFACompatibilityPolicy=1']

def convert(file_src_path, dest_path):
    cwd = os.getcwd()
    os.chdir(os.path.dirname(dest_path))
    try:
        subprocess.check_output(gs_command + ['-sOutputFile=' + dest_path , file_src_path])
        os.remove(file_src_path)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("'{}' returned the following error: (code {}): {}".format(e.cmd, e.returncode, e.output))

    os.chdir(cwd)

for dirname, subdirs, files in os.walk(source_dir):
    for file in [f for f in files if f.upper().endswith("PDF")]:
        full_path = os.path.join(dirname, file)
        full_dest_path = os.path.join(destination_dir, os.path.basename(full_path))
        print("Converting File: {}".format(full_path))
        convert(full_path, full_dest_path)

