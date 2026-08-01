
def tab_in_leading(s):
    """Returns True if there are tabs in the leading whitespace of a line,
    including the whitespace of docstring code samples."""
    n = len(s) - len(s.lstrip())
    if not s[n:n + 3] in ['...', '>>>']:
        check = s[:n]
    else:
        smore = s[n + 3:]
        check = s[:n] + smore[:len(smore) - len(smore.lstrip())]
    return not (check.expandtabs() == check)

