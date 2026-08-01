
def parse_fuzzy_compare(source):
    "Parses a cost comparator."
    if source.match("<="):
        return True
    elif source.match("<"):
        return False
    else:
        return None

