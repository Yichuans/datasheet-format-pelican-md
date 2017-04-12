# -*- coding: utf-8 -*-
import unittest
import string
from regx import process_line

class regx_test2(unittest.TestCase):
    def setUp(self):
        self.dummy_value = ''
        self.expected_value = ''
        self.calculated_value = ''

    def tearDown(self):
        self.setUp()

    def compare_equal(self):
        self.calculated_value = process_line(self.dummy_value)

        self.assertEqual(self.expected_value, self.calculated_value,
            msg='raw_value:\n {} expect value:\n {} does not equal to regx replaced value:\n {}'.format(self.dummy_value, 
                self.expected_value, 
                self.calculated_value))

    def test_remove_asterisks_around_headings(self):
        self.dummy_value = '**HUUU**\n======='
        self.expected_value = 'HUUU\n======='

        self.compare_equal()

    def test_remove_asterisks_around_single_char(self):
        """Test case like **.** -> . """

        for value in string.printable[:-5]:

            dummy_value1 = 'yh**{}**'.format(value)
            dummy_value2 = 'yh*{}*'.format(value)

            self.expected_value = 'yh' + value

            for dummy_value in (dummy_value1, dummy_value2):
                self.dummy_value = dummy_value
                self.compare_equal()

    def test_convert_superscript(self):

        self.dummy_value = "^aaa^"
        self.expected_value = "<sup>aaa</sup>"
        
        self.compare_equal()

    def test_remove_trailing_or_preceding_white_space(self):

        self.dummy_value = '** imj *'
        self.expected_value = "**imj*"

        self.compare_equal()


    def test_check_multiple_conditions_in_a_single_line(self):

        self.dummy_value = "** jicme ** ccc ^sup^*.*"
        self.expected_value = "**jicme** ccc <sup>sup</sup>."

        self.compare_equal()

    def test_in_text_removing_preceding_white_space(self):
        self.dummy_value = """
        The islands are one of the least disturbed major cool-temperate island ecosystems in the south Atlantic. The flora of both is typical of southern cold-temperate oceanic islands with their relatively low species diversity and a preponderance of ferns and cryptogams. On ** Gough Island** there
        """
        self.expected_value = """
        The islands are one of the least disturbed major cool-temperate island ecosystems in the south Atlantic. The flora of both is typical of southern cold-temperate oceanic islands with their relatively low species diversity and a preponderance of ferns and cryptogams. On **Gough Island** there
        """

        self.compare_equal()

    def test_in_text_check_multiple_conditions(self):

        self.dummy_value = """Roth, H. *et* *al*. (1979). *Etat Actuel des Parcs Nationaux de la Comoé et de Taï Ainsi que de la Réserve d'Azagny et Propositions Visant à leur Conservation.* *Tome 4*. FGU-Kronberg GMBH*,* Abidjan.

        Roth, H., Merz, G. & Steinhauer, B. (1984). Distribution and status of large mammals in Ivory Coast. 1. Introduction. *Mammalia* 48(2): 207-226.
        """
        self.expected_value = """Roth, H. *et al*. (1979). *Etat Actuel des Parcs Nationaux de la Comoé et de Taï Ainsi que de la Réserve d'Azagny et Propositions Visant à leur Conservation. Tome 4*. FGU-Kronberg GMBH, Abidjan.

        Roth, H., Merz, G. & Steinhauer, B. (1984). Distribution and status of large mammals in Ivory Coast. 1. Introduction. *Mammalia* 48(2): 207-226.
        """

        self.compare_equal()

    def test_in_text_check_multiple_conditions_2(self):

        self.dummy_value = """*Gough Island, in the South Atlantic, is one of the least disrupted cool temperate island ecosystems in the world. The towering cliffs are home to one of the world's largest colonies of sea birds. The island also has two endemic species of land bird, the Gough moorhen and the Gough finch, four endemic vascular plants and 15 endemic ferns.*

            *Inaccessible Island is part of the Tristan da Cunha-Gough Island group, 350 kilometres north-northwest of Gough Island. It is largely pristine and is one of the few temperate oceanic islands free of introduced mammals. It has two birds, eight plants and ten invertebrates found nowhere else. 70 terrestrial plant and animal species are restricted to the islands and 60 marine species are endemic to the island group. *

            COUNTRY
            -------
        """
        self.expected_value = """*Gough Island, in the South Atlantic, is one of the least disrupted cool temperate island ecosystems in the world. The towering cliffs are home to one of the world's largest colonies of sea birds. The island also has two endemic species of land bird, the Gough moorhen and the Gough finch, four endemic vascular plants and 15 endemic ferns.*

            *Inaccessible Island is part of the Tristan da Cunha-Gough Island group, 350 kilometres north-northwest of Gough Island. It is largely pristine and is one of the few temperate oceanic islands free of introduced mammals. It has two birds, eight plants and ten invertebrates found nowhere else. 70 terrestrial plant and animal species are restricted to the islands and 60 marine species are endemic to the island group.*

            COUNTRY
            -------
        """
        self.compare_equal()

    def test_in_text_check_multiple_conditions_3(self):

        self.dummy_value = """**STATEMENT OF OUTSTANDING** UNIVERSAL VALUE [pending]
------------------------------------------------------

IUCN MANAGEMENT **CATEGORY**
----------------------------

II National Park

BIOGEOGRAPHICAL **PROVINCE**
----------------------------

Guyanan (8.04.01)

**GEOGRAPHICAL LOCATION** 
--------------------------
        """

        self.expected_value = """STATEMENT OF OUTSTANDING UNIVERSAL VALUE [pending]
------------------------------------------------------

IUCN MANAGEMENT CATEGORY
----------------------------

II National Park

BIOGEOGRAPHICAL PROVINCE
----------------------------

Guyanan (8.04.01)

GEOGRAPHICAL LOCATION 
--------------------------
        """


        self.compare_equal()

    def test_in_text_check_multiple_conditions_4(self):

        self.dummy_value = """**NATURAL** WORLD HERITAGE SITE
-------------------------------

1994: Proposed for inscription on the World Heritage List under Natural Criteria vii, viii, ix and x.

**STATEMENT OF OUTSTANDING** UNIVERSAL VALUE [pending]
------------------------------------------------------

IUCN MANAGEMENT **CATEGORY**
----------------------------
        """

        self.expected_value = """NATURAL WORLD HERITAGE SITE
-------------------------------

1994: Proposed for inscription on the World Heritage List under Natural Criteria vii, viii, ix and x.

STATEMENT OF OUTSTANDING UNIVERSAL VALUE [pending]
------------------------------------------------------

IUCN MANAGEMENT CATEGORY
----------------------------
        """


        self.compare_equal()



if __name__=='__main__':
    unittest.main()
