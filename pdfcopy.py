#!/usr/bin/env python

import os
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter

pdf_input = None
pdf_output = None


def open_file(path, file_password):
    pdf_input = PdfFileReader(open(path, "rb"))

    if pdf_input.isEncrypted is True:
        print("File is encrypted")
        if file_password is not None:
            pdf_input.decrypt(file_password)

    return pdf_input


def make_copy(pdf_file, pdf_path):
    pdf_output = PdfFileWriter()

    file_name, file_extension = os.path.splitext(pdf_path)
    file_name_new = file_name + '-new'
    path_new = file_name_new + file_extension

    for page in pdf_file.pages:
        pdf_output.addPage(page)

    output_stream = open(path_new, "wb")
    pdf_output.write(output_stream)

    return output_stream


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    pdf_password = None

    if len(sys.argv) > 2:
        pdf_password = sys.argv[2]

    f = open_file(pdf_path, pdf_password)
    fn = make_copy(f, pdf_path)
