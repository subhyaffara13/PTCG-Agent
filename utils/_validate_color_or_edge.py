
def _validate_color_or_edge(s):
    if cbook._str_equal(s, 'edge'):
        return s
    return validate_color(s)

