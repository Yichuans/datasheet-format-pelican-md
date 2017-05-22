import os
import subprocess


# construct pandoc commandline
def pandoc_convert(input_file, output_file):
	args = ['pandoc', '-s', input_file, '--wrap=none', '-t', 'markdown-multiline_tables-simple_tables-pipe_tables-grid_tables',
	'-o', output_file]

	subprocess.call(args)


def main(input_path, output_path):
	# walk through docx folder
	for docx_name in os.listdir(input_path):
		input_file = input_path + os.sep + docx_name
		output_file = output_path + os.sep + docx_name.split('.')[0] + '.md'

		pandoc_convert(input_file, output_file)


if __name__ == '__main__':
	# create output folder
	INPUT_PATH = 'DOCX_original_2017'
	INPUT_PATH = 'DOCX_original_20170518'
	OUTPUT_PATH = 'MD_pandoc'
	if not os.path.exists(OUTPUT_PATH):
		os.mkdir(OUTPUT_PATH)

	main(INPUT_PATH, OUTPUT_PATH)