import re

INTEGER_REGEXS = [
    re.compile(r'(?P<Type>\d*)', re.IGNORECASE)  
]

BOOLEAN_REGEXS = [
    re.compile(r'(?P<Type>[0-1])\|', re.IGNORECASE)  
]

STRING_REGEXS = [
    # (E)thernet to the cell site - (P)lanning and (D)esign (D)atabase
    re.compile(r'(?P<Type>[^\|\d])', re.IGNORECASE),
    # ma0585
    re.compile(r'(?P<Type>[a-z]+[0-9]+)', re.IGNORECASE),
    # 05/01/2020
    re.compile(r'(?P<Type>\d{2}\/\d{2}\/\d{4})', re.IGNORECASE),
]

TYPE_REGEXS = {
    'String': STRING_REGEXS,
    'int': INTEGER_REGEXS,
    'boolean': BOOLEAN_REGEXS,
}


def parse_type(type_str, header):
    for info_type in TYPE_REGEXS:
        for regex in TYPE_REGEXS[info_type]:
            m = re.search(regex, type_str)

            if m is None:
                continue

            return info_type
