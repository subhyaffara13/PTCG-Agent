
def parse_constraint(source, constraints, ch):
    "Parses a constraint."
    if ch not in "deis":
        raise ParseError()

    if ch in constraints:
        raise ParseError()

    return ch

