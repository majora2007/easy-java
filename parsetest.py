import unittest
from parse import DataParser
from rule import ParseRule
from languagetype import Language, LanguageType


class Test_TestParse(unittest.TestCase):
    def test_parse_type(self):
        parser = DataParser()
        self.assertEqual(parser.parse_type('Hippos eat grass'), LanguageType.string)
        self.assertEqual(parser.parse_type('0123'), LanguageType.string)
        self.assertEqual(parser.parse_type('0.43'), LanguageType.float)
        self.assertEqual(parser.parse_type('.32'), LanguageType.float)
        self.assertEqual(parser.parse_type('100'), LanguageType.integer)
        self.assertEqual(parser.parse_type('$650 Switcher registration'), LanguageType.string)
    
    def test_parse_type_translate(self):
        parser = DataParser()
        self.assertEqual(parser.translate_type(LanguageType.string, Language.Java), 'String')
        self.assertEqual(parser.translate_type(LanguageType.string, Language.Typescript), 'string')
        self.assertEqual(parser.translate_type(LanguageType.integer, Language.Typescript), 'number')
    
    def test_parse_type_order(self):
        """ Test parsing a type where I order a BigInt mapping in front of int """
        parser = DataParser()
        rules = parser.rules
        rules.insert(0, ParseRule('matches', r'\d*', 'BigInt'))
        parser.rules = rules

        self.assertEqual(parser.parse_type('100'), 'BigInt')


        

if __name__ == '__main__':
    unittest.main()
