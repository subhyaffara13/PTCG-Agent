
def _validate_color_or_None(s):
    if s is None or cbook._str_equal(s, "None"):
        return None
    return validate_color(s)

