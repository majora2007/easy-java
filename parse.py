from rule import ParseRule, RenameRule
from languagetype import LanguageType, Language

default_rules = [
    # (E)thernet to the cell site - (P)lanning and (D)esign (D)atabase
    ParseRule('matches', r'[^\|\d\.]*', LanguageType.string),
    # ma0585
    ParseRule('matches', r'[a-z]+[0-9]+', LanguageType.string),
    # 05/01/2020
    ParseRule('matches', r'\d{2}\/\d{2}\/\d{4}', LanguageType.string),
    # 0123
    ParseRule('matches', r'0\d+', LanguageType.string),
    # 0.234
    ParseRule('matches', r'\d?\.\d*', LanguageType.float),
    # 123
    ParseRule('matches', r'\d*', LanguageType.integer),
]

java_rename_rules = [
    RenameRule(LanguageType.string, 'String'),
    RenameRule(LanguageType.integer, 'int'),
    RenameRule(LanguageType.float, 'float'),
]

typescript_rename_rules = [
    RenameRule(LanguageType.string, 'string'),
    RenameRule(LanguageType.integer, 'number'),
    RenameRule(LanguageType.float, 'number'),
]


language_type_rules = {
    Language.Java: java_rename_rules,
    Language.Typescript: typescript_rename_rules
}


class DataParser(object):
    """ Responsible for infering text values into language types based on a set of rules """

    rules = []

    def __init__(self, rules=default_rules):
        self.rules = rules

        # Add a catchall for NoneTypes, but prioritize order of rulelist
        self.rules.append(ParseRule('matches', r'.*', LanguageType.string))

    def parse_type(self, value):
        for rule in self.rules:
            parsed_type = rule.run(value)

            if parsed_type is not None:
                return parsed_type
        return None

    def translate_type(self, parse_type, language):
        if not language in language_type_rules:
            return parse_type
        
        rules = language_type_rules[language]
        
        for rename in rules:
            translated_type = rename.run(parse_type)
            if translated_type is None:
                continue
            return translated_type
        return parse_type
