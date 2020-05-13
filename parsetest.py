import unittest
import parse


class Test_TestParse(unittest.TestCase):
    def test_parse_type(self):
        self.assertEqual(parse.parse_type('Hippos eat grass'), 'String')
        self.assertEqual(parse.parse_type('0123'), 'String')
        self.assertEqual(parse.parse_type('0.43'), 'float')
        self.assertEqual(parse.parse_type('.32'), 'float')
        self.assertEqual(parse.parse_type('100'), 'int')
        

if __name__ == '__main__':
    unittest.main()
