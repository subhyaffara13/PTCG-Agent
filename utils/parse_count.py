
def parse_count(source):
    "Parses a quantifier's count, which can be empty."
    return source.get_while(DIGITS)

