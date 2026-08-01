
def parse_quantifier(source, info, ch):
    "Parses a quantifier."
    q = _QUANTIFIERS.get(ch)
    if q:
        # It's a quantifier.
        return q

    if ch == "{":
        # Looks like a limited repeated element, eg. 'a{2,3}'.
        counts = parse_limited_quantifier(source)
        if counts:
            return counts

    return None

