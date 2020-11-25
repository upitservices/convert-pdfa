try:
    from PIL import Image
except ImportError:
    import Image

import subprocess
import datetime
import os
import re
import pytesseract
import random
from pathlib import Path

class Ocr():

    gs_executable = None
    source_dir = None
    destination_dir = None
    destination_dir_img = None

    def __init__(self, confs):
        self.gs_executable = confs['gs_executable']
        self.source_dir = confs['source_dir']
        self.destination_dir = confs['destination_dir_ocr']
        self.destination_dir_img = confs['destination_dir_img']
        pytesseract.pytesseract.tesseract_cmd = confs['tesseract_executable']

    def pdf_to_tiff(self, file_src_path, dest_path):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(dest_path))

        try:
            gs_command = [self.gs_executable,  '-dBATCH', '-dNOPAUSE', '-sDEVICE=tiff24nc', '-r300']
            subprocess.check_output(gs_command + ['-sOutputFile="' + dest_path + '"', file_src_path])
        except subprocess.CalledProcessError as e:
            raise RuntimeError("'{}' returned the following error: (code {}): {}".format(e.cmd, e.returncode, e.output))

        os.chdir(cwd)

    def convert_file(self, file_path, keep_filename = False):
        str_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_hash = random.getrandbits(128)
        filename = "converted-{}-{}.pdf".format(random_hash, str_date_time)
        full_dest_path = os.path.join(self.destination_dir_img, os.path.basename(file_path))
        full_dest_path = re.sub(r'(\.pdf)', r'.tif', full_dest_path).lower()
        self.pdf_to_tiff(file_path, full_dest_path)

        if keep_filename:
            filename = os.path.basename(file_path)

        return self.save_resulting_pdf(full_dest_path, filename)
    
    def convert_folder(self, keep_filename = False):
        for dirname, subdirs, files in os.walk(self.source_dir):
            for file in [f for f in files if f.upper().endswith("PDF")]:
                full_path = os.path.join(dirname, file)
                self.convert_file(full_path, keep_filename)

    def save_resulting_pdf(self, tiff_path, filename):
        try:
            pdf = pytesseract.image_to_pdf_or_hocr(tiff_path, extension='pdf')
            pdf_path = os.path.join(self.destination_dir, filename)
            with open(pdf_path, 'w+b') as f:
                f.write(pdf)
            
            # Removing the tiff source
            os.remove(tiff_path)
            # @todo: Check if the final PDF was really generated. Then, based on the user choice, remove the source path
            return pdf_path
        except:
            print("Error while converting file: {}".format(filename))

        
