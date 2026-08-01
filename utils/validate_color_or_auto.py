
def validate_color_or_auto(s):
    if cbook._str_equal(s, 'auto'):
        return s
    return validate_color(s)

