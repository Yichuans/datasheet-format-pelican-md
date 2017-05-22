import os
import sys
from pandoc_docx_md import pandoc_convert
from convert_datasheet_pelican_format import datasheet


def main(input_folder, output_folder):
    pandoc_temp = output_folder + os.sep + 'pandoc_temp'

    if not os.path.exists(input_folder):
        raise Exception('Input folder: "{}" does not exist'.format(input_folder))

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    if not os.path.exists(pandoc_temp):
        os.mkdir(pandoc_temp)

    for docx_name in os.listdir(input_folder):
        # convert via pandoc
        input_file = input_folder + os.sep + docx_name
        pandoc_file = pandoc_temp + os.sep + docx_name.split('.')[0] + '.md'
        pandoc_convert(input_file, pandoc_file)

        # clean pandoc md
        ds = datasheet(pandoc_file)
        ds.save_to_folder(output_folder)

if __name__ == '__main__':
    input_folder = 'DOCX_original_20170519EDIT'
    # input_folder = 'DOCX_original_20170522'
    # output_folder = 'MD_ready'
    output_folder = 'MD_edit'

    main(input_folder, output_folder)
