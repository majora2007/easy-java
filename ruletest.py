import unittest
from rule import ParseRule, RenameRule


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

    def test_rename_rule(self):
        java_rename_rules = [
            RenameRule('Java', 'string', 'String'),
            RenameRule('Java', 'integer', 'int'),
            RenameRule('Java', 'float', 'float'),
        ]
        self.assertEqual(java_rename_rules[0].run('string'), 'String')
        self.assertEqual(java_rename_rules[1].run('integer'), 'int')
        self.assertEqual(java_rename_rules[0].run('hippo'), None)

if __name__ == '__main__':
    unittest.main()
