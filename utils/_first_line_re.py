
def _first_line_re():
    """
    Return a regular expression based on first_line_re suitable for matching
    strings.
    """
    if isinstance(first_line_re.pattern, str):
        return first_line_re

    # first_line_re in Python >=3.1.4 and >=3.2.1 is a bytes pattern.
    return re.compile(first_line_re.pattern.decode())

