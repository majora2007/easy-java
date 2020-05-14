import unittest
from parse import DataParser


class Test_TestParse(unittest.TestCase):
    def test_parse_type(self):
        parser = DataParser()
        self.assertEqual(parser.parse_type('Hippos eat grass'), 'String')
        self.assertEqual(parser.parse_type('0123'), 'String')
        self.assertEqual(parser.parse_type('0.43'), 'float')
        self.assertEqual(parser.parse_type('.32'), 'float')
        self.assertEqual(parser.parse_type('100'), 'int')
        

if __name__ == '__main__':
    unittest.main()
