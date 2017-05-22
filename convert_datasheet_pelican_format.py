import os
import codecs
import markdown
import re
from time import gmtime, strftime
from bs4 import BeautifulSoup, element
from fuzzywuzzy import process, fuzz
from regx import process_line



class datasheet(object):
    def __init__(self, infile):
        self._file_name = os.path.basename(infile)
        with codecs.open(infile, mode='r', encoding='utf-8') as f:
        # default
            self.raw_md = f.read()

        self.md = self._process_md()
        self.title = ''
        self.country = []
        self.author = 'UNEP-WCMC'
        self.year = ''
        # soup
        html = markdown.markdown(self.md)
        self._soup = BeautifulSoup(html, "html5lib")
        self._hs = self._soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
        # get attribute
        self._find_title_country()
        self._find_year()

    def __repr__(self):
        return self.metadata()


    def _process_md(self):
        # remove first two lines of image
        temp_list = self.raw_md.split('\n')
        raw_md = '\n'.join(temp_list[2:])

        return process_line(raw_md)

    def metadata(self):
        return u"Title: {0}\nTags: {1}\nAuthor: {2}\nYear: {3}\nDate: {4}".format(self.title, 
            ','.join(self.country), 
            self.author, 
            self.year,
            strftime("%Y-%m-%d %H:%M:%S", gmtime()))


    def _find_title_country(self):
        # scenario title, country in h1
        h1 = self._soup.find_all('h1')
        if len(h1) == 2:
            self.title = h1[0].get_text().strip()
            self.country = map(unicode.strip, h1[1].get_text().split('&'))

            return

        # scenario not in h1, look for other headings
        # best guess of country ===
        country_tag, _ = process.extractOne('country', self._hs)
        country = self._find_next_sibling(country_tag)
        if isinstance(country, element.Tag):
            self.country = map(unicode.strip, country.get_text().split('and'))

        # best guess of title ===
        title_tag, _ = process.extractOne('name', self._hs)
        title = self._find_next_sibling(title_tag)
        if isinstance(title, element.Tag):
            self.title = title.get_text().strip()

    def _find_year(self):
        # regular expression, starting four digits
        year_regex = re.compile('^[0-9]{4}')

        year_tag, _ = process.extractOne('NATURAL WORLD HERITAGE SITE', self._hs, scorer=fuzz.token_set_ratio)
        year = self._find_next_sibling(year_tag)

        # debug
        # if year.string is None:
        #   global cc
        #   cc = year

        if isinstance(year, element.Tag):
            all_years = re.findall(year_regex, year.get_text())
            if len(all_years)>0:
                self.year = all_years[0]
                # global dd
                # dd = year
            else:
                print 'warning:', self.title, self.country, 'has no year information'

    def _find_next_sibling(self, tag):
        # find the first non '\n' sibling
        for sibling in tag.next_siblings:
            if sibling == '\n':
                pass
            else:
                return sibling
                break

        return None

    def save_as_pelican_md(self, outfile=None):
        outfile = outfile or 'pelican_' + self._file_name
        outmd = self.metadata() + '\r\n\r\n' + self.md
        with codecs.open(outfile, mode='w', encoding='utf-8') as f:
            f.write(outmd)

    def save_to_folder(self, outpath):
        outfile = outpath + os.sep + 'pelican_' + self._file_name
        self.save_as_pelican_md(outfile)

def main():
    INPUT_PATH = 'MD_pandoc'
    OUTPUT_PATH = 'MD_ready'

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    for each in os.listdir(INPUT_PATH):
        if each.endswith('.md'):
            ds = datasheet(INPUT_PATH + os.sep + each)
            ds.save_to_folder(OUTPUT_PATH)

if __name__ == '__main__':
    main()