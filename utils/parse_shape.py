
def parse_shape(docstring):
    match = _re_shape.search(docstring)
    if match:
        return " " + match.group(1)
    return None

