from rule import ParseRule


default_rules = [
    # (E)thernet to the cell site - (P)lanning and (D)esign (D)atabase
    ParseRule('matches', r'[^\|\d\.]*', 'String'),
    # ma0585
    ParseRule('matches', r'[a-z]+[0-9]+', 'String'),
    # 05/01/2020
    ParseRule('matches', r'\d{2}\/\d{2}\/\d{4}', 'String'),
    # 0123
    ParseRule('matches', r'0\d+', 'String'),
    # 0.234
    ParseRule('matches', r'\d?\.\d*', 'float'),
    # 123
    ParseRule('matches', r'\d*', 'int'),
]

class DataParser(object):
    """ Responsible for infering text values into language types based on a set of rules """

    rules = []

    def __init__(self, rules=default_rules):
        self.rules = rules

    def parse_type(self, value):
        for rule in self.rules:
            parsed_type = rule.run(value)

            if parsed_type is not None:
                return parsed_type
        return None

""" def parse_type(value):
    for rule in default_rules:
        parsed_type = rule.run(value)
        if parsed_type is not None:
            return parsed_type """

