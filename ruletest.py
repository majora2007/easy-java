import unittest
from rule import Rule, ParseRule


class Test_TestRule(unittest.TestCase):
    def test_parse_rule(self):
        rule = ParseRule('endswith', 'Id', 'int')

        self.assertEqual(rule.run('AppId'), 'int')
        self.assertEqual(rule.run('App'), None)

        rule = ParseRule('matches', r'[^\|\d\.]*', 'String')
        self.assertEqual(rule.run('Hippos are cool'), 'String')
        self.assertEqual(rule.run('1234'), None)
    
    def test_parse_rule_description(self):
        rule = ParseRule('endswith', 'Id', 'int')
        self.assertEqual(rule.description(), 'On Parse: VALUE endswith Id, return int')

        rule = ParseRule('contains', '"', 'String')
        self.assertEqual(rule.description(), 'On Parse: VALUE contains ", return String')

        

if __name__ == '__main__':
    unittest.main()
