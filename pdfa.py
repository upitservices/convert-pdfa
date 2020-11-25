try:
    from PIL import Image
except ImportError:
    import Image

import subprocess
import datetime
import os
import re
import random
from pathlib import Path

class PdfA():

    gs_executable = None
    source_dir = None
    destination_dir = None
    destination_dir_img = None
    destination_dir_ocr = None

    def __init__(self, confs):
        self.gs_executable = confs['gs_executable']
        self.source_dir = confs['source_dir']
        self.destination_dir = confs['destination_dir']
        self.destination_dir_img = confs['destination_dir_img']
        self.destination_dir_ocr = confs['destination_dir_ocr']

    def convert(self, file_src_path, dest_path, delete_original = False):
        gs_command = [self.gs_executable, '-dPDFA', '-dBATCH', '-dNOPAUSE', 
                        '-sColorConversionStrategy=UseDeviceIndependentColor',
                        '-sDEVICE=pdfwrite', '-dPDFACompatibilityPolicy=1']

        cwd = os.getcwd()
        os.chdir(os.path.dirname(dest_path))
        try:
            subprocess.check_output(gs_command + ['-sOutputFile=' + dest_path , file_src_path])
            if delete_original:
                os.remove(file_src_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("'{}' returned the following error: (code {}): {}".format(e.cmd, e.returncode, e.output))

        os.chdir(cwd)

    def convert_file(self, file_path, delete_original = False, keep_filename = False):
        str_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_hash = random.getrandbits(128)
        filename = "converted-{}-{}.pdf".format(random_hash, str_date_time)

        if keep_filename:
            filename = os.path.basename(file_path)

        full_dest_path = os.path.join(self.destination_dir, filename)
        self.convert(file_path, full_dest_path, delete_original)
    
    def convert_folder(self, keep_filename = False, origin_ocr = False):
        source_dir = self.source_dir if origin_ocr == False else self.destination_dir_ocr
        delete_original = origin_ocr
        for dirname, subdirs, files in os.walk(source_dir):
            for file in [f for f in files if f.upper().endswith("PDF")]:
                full_path = os.path.join(dirname, file)
                self.convert_file(full_path, delete_original, keep_filename)