
def subfn(pattern, format, string, count=0, flags=0, pos=None, endpos=None,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Return a 2-tuple containing (new_string, number). new_string is the string
    obtained by replacing the leftmost (or rightmost with a reverse pattern)
    non-overlapping occurrences of the pattern in the source string by the
    replacement format. number is the number of substitutions that were made. format
    can be either a string or a callable; if a string, it's treated as a format
    string; if a callable, it's passed the match object and must return a
    replacement string to be used."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.subfn(format, string, count, pos, endpos, concurrent, timeout)

