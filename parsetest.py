import unittest
from parse import DataParser
from rule import ParseRule


class Test_TestParse(unittest.TestCase):
    def test_parse_type(self):
        parser = DataParser()
        self.assertEqual(parser.parse_type('Hippos eat grass'), 'String')
        self.assertEqual(parser.parse_type('0123'), 'String')
        self.assertEqual(parser.parse_type('0.43'), 'float')
        self.assertEqual(parser.parse_type('.32'), 'float')
        self.assertEqual(parser.parse_type('100'), 'int')
    
    def test_parse_type_order(self):
        """ Test parsing a type where I order a BigInt mapping in front of int """
        parser = DataParser()
        rules = parser.rules
        rules.insert(0, ParseRule('matches', r'\d*', 'BigInt'))
        parser.rules = rules

        self.assertEqual(parser.parse_type('100'), 'BigInt')


        

if __name__ == '__main__':
    unittest.main()
