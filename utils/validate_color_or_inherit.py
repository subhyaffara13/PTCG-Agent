
def validate_color_or_inherit(s):
    """Return a valid color arg."""
    if cbook._str_equal(s, 'inherit'):
        return s
    return validate_color(s)

