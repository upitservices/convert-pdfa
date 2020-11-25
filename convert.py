import os
import json
import sys
import argparse
from pathlib import Path
from ocr import Ocr
from pdfa import PdfA

class Main():

    confs = None

    def __init__(self):
        self.read_config()

    def read_config(self):
        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.split(path_to_current_file)[0]
        conf_path = os.path.join(current_directory, "conf.json")

        with open(conf_path, encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.confs = {
                'source_dir': Path(data['source_dir']),
                'destination_dir': Path(data['destination_dir']),
                'destination_dir_img': Path(data['destination_dir_img']),
                'destination_dir_ocr': Path(data['destination_dir_ocr']),
                'gs_executable': r"{}".format(data['gs_executable']),
                'tesseract_executable': r"{}".format(data['tesseract_executable']),
            }

        if not data or not self.confs['source_dir'] or not self.confs['gs_executable']:
            print('Missing config parameters')
            return False

        return True

    def execute(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--file', help='PDF file to be converted')
        parser.add_argument('--ocr', help='true to make the PDF searchable before converting to PDF/A')
        parser.add_argument('--keep_filename', help='true to keep the original filename after conversion')
        args = parser.parse_args()

        filePath = None

        if args.ocr == 'true':
            ocr = Ocr(self.confs)
            if args.file == None:
                ocr.convert_folder(True if args.keep_filename == 'true' else False)
            else:
                filePath = ocr.convert_file(args.file, True if args.keep_filename == 'true' else False)
        
        pdfa = PdfA(self.confs)
        if args.file == None and filePath == None:
            keep_filename = True if args.keep_filename == 'true' else False
            origin_ocr = True if args.ocr == 'true' else False
            pdfa.convert_folder(keep_filename, origin_ocr)
        else:
            delete_original = True # @todo: Create a parameter, so the user can choose
            keep_filename = True if args.keep_filename == 'true' else False
            if filePath == None:
                filePath = args.file
            pdfa.convert_file(filePath, delete_original, keep_filename)

main = Main()
main.execute()