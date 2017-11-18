import os
import re
import subprocess
import sys
from PyPDF2 import PdfFileReader


class PdfParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdfpy2_obj = None
        self.re_match_rule = None
        self.contents = []
        self.open_file()

    def open_file(self):
        file_obj = open(self.pdf_path, 'rb')

        try:
            pdf = PdfFileReader(file_obj)
        except Exception as e:
            # Assume the exception is due to a corrupted PDF file
            new_path = self.repair_pdf(self.pdf_path)
            file_obj = open(new_path, 'rb')
            pdf = PdfFileReader(file_obj)

        self.pdfpy2_obj = pdf
        self.populate_contents()

    def populate_contents(self):
        for page in self.pdfpy2_obj.pages:
            self.contents.append(page.extractText())

    def get_content_for_page_n(self, page_n):
        return self.contents[page_n]

    def set_re_match_rule(self, regex):
        self.re_match_rule = re.compile(regex, re.MULTILINE|re.S)

    def get_matches(self, page_n):
        return re.findall(self.re_match_rule, self.contents[page_n])
        # return self.contents[page_n].findall(self.re_match_rule)

    @staticmethod
    def repair_pdf(path):
        file_name, file_extension = os.path.splitext(path)
        file_name_new = file_name + '-repaired'
        pdf_path_new = file_name_new + file_extension

        # Use Ghostscript to repair the PDF file
        subprocess.run(['gs', '-o', pdf_path_new, '-sDEVICE=pdfwrite', '-dPDFSETTINGS=/prepress', path],
                       stdout=subprocess.DEVNULL)

        return pdf_path_new


def main(path):
    """Example usage of the PdfParser class"""
    pp = PdfParser(path)
    pp.set_re_match_rule('Closing Balance(\$[0-9,\.]+)')
    pp.open_file()
    matches = pp.get_matches(0)
    print(matches[0])


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    main(pdf_path)