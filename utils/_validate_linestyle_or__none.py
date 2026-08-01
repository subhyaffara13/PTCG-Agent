
def _validate_linestyle_or_None(s):
    if s is None or cbook._str_equal(s, "None"):
        return None

    return _validate_linestyle(s)

