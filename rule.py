import re
from languagetype import LanguageType

class Rule(object):
    """ A Rule is a base class for performing some action. An example of a rule is when parsing, if field ends in Id, map to int. """

    enabled = True

    def __init__(self):
        pass
    
    def description(self):
        pass

    def run(self, value):
        pass

class ParseRule(Rule):

    comparison = '' # endswith, startswith, contains, matches (Can be a enum)
    comparedTo = '' # what should go in the comparison


    def __init__(self, comparison, comparedTo, mapTo):
        super().__init__()
        self.comparison = comparison
        self.comparedTo = comparedTo
        self.mapTo = mapTo

    def run(self, value):
        super().run(value)
        if self.comparison == 'endswith':
            if value.endswith(self.comparedTo):
                return self.mapTo
        elif self.comparison == 'startswith':
            if value.startswith(self.comparedTo):
                return self.mapTo
        elif self.comparison == 'contains':
            if self.comparedTo in value:
                return self.mapTo
        elif self.comparison == 'matches':
            regex = re.compile(r'(?P<Type>' + self.comparedTo + ')', re.IGNORECASE)
            m = re.search(regex, value)
            
            if m is None:
                return None
            elif len(m.group('Type')) is not len(value):
                return None

            return self.mapTo
            
        return None
    
    def description(self):
        return 'On Parse: VALUE {0} {1}, return {2}'.format(self.comparison, self.comparedTo, self.mapTo)
        
class RenameRule(Rule):
    """ Used to map a LanguageType (generic enum) to an actual string """

    def __init__(self, source, target):
        super().__init__()
        self.source_type = source
        self.target_type = target

    def description(self):
        return 'On Rename: {1} -> {2}'.format(self.source_type, self.target_type)

    def run(self, source):
        if source == self.source_type:
            return self.target_type
        return None

