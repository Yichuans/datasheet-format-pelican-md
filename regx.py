import re

# render correct superscript
# ^rd^ -> 	<sup>rd</sup>
pattern_super_script = re.compile(r"\^(.+?)\^")
replace_super_script = r"<sup>\1</sup>"

# remove asterisks surrounding singles  
# xxx*.* ->	xxx.
pattern_single_char_between_asterisk = re.compile(r"(?<=\S)\*+(.)\*+")
replace_single_char_between_asterisk = r"\1"

# remove space between asterisks 
# ** xxxx ** ->	**xxxx**
pattern_italic_bold = re.compile(r"(\*+) *?(\S.+?\S) *?(\*+)")
replace_italic_bold = r"\1\2\3"

# remove asterisks surround Headings
# **UUUU **	  -> UUUU
pattern_heading = re.compile(r"(\*+((?=.*\n-)|(?=.*\n=)))")
replace_heading = r""

rules = ((pattern_super_script, replace_super_script),
(pattern_single_char_between_asterisk, replace_single_char_between_asterisk),
(pattern_italic_bold, replace_italic_bold),
(pattern_heading, replace_heading))

def process_line(line):
	newline = ''

	for rule in rules:
		pattern = rule[0]
		replace = rule[1]

		if newline: 
			newline = pattern.sub(replace, newline)
		else:
			newline = pattern.sub(replace, line)

	return newline


