
def parse_default(docstring):
    match = _re_default.search(docstring)
    if match:
        return " " + match.group(1)
    return None

