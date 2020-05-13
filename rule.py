class Rule(object):
    """ A Rule is a base class for performing some action. An example of a rule is when parsing, if field ends in Id, map to int. """

    enabled = True

    def __init__(self):
        pass
    
    def description(self):
        pass

class ParseRule(Rule):

    comparison = '' # endswith, startswith, contains (Can be a enum)
    comparedTo = '' # what should go in the comparison



    def __init__(self, comparison, comparedTo, mapTo):
        super().__init__()
        self.comparison = comparison
        self.comparedTo = comparedTo
        self.mapTo = mapTo

    def run(self, value):
        if self.comparison == 'endswith':
            if value.endswith(self.comparedTo):
                return self.mapTo
        return None
    
    def description(self):
        return "On Parse, "
        
    
