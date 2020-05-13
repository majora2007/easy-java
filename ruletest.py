import unittest
from rule import Rule, ParseRule


class Test_TestRule(unittest.TestCase):
    def test_parse_rule(self):
        rule = ParseRule('endswith', 'Id', 'int')
        
        self.assertEqual(rule.run('AppId'), 'int')
        self.assertEqual(rule.run('App'), None)

        

if __name__ == '__main__':
    unittest.main()
