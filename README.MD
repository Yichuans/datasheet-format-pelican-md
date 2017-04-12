# UNEP-WCMC World Heritage Datasheet

This repository holds the methodology to convert the aging datasheets in DOCX format to markdown, enabling easy publishing based on Pelican.

## Methodology

- Convert the documents using `pandoc`. Use python `subprocess.call` to run commands such as `pandoc -s Brazil\ -\ Atlantic\ Forest\ South-East.docx --wrap=none -t Markdown-multiline_tables-simple_tables-pipe_tables-grid_tables -o test.md`. Note constructing the command in text requires proper escapes. One could specific

```python
args = ['pandoc', '-s', input_file, '--wrap=none', '-t', 'markdown-multiline_tables-simple_tables-pipe_tables-grid_tables',
	'-o', output_file]
subprocess.call(args)

```

- To ensure the resulting documents could be used by Pelican, it is imperative that minimal metadata is constructed by reading the content. See the script `convert-datasheet-pelican-format.py` for details 

- Due to the nature of inconsistent formatting in the original word document, the resulting document in markdown needs cleaning. Notably markdown italic and bold seem to have been messed up.