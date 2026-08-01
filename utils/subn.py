
def subn(pattern, repl, string, count=0, flags=0, pos=None, endpos=None,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Return a 2-tuple containing (new_string, number). new_string is the string
    obtained by replacing the leftmost (or rightmost with a reverse pattern)
    non-overlapping occurrences of the pattern in the source string by the
    replacement repl. number is the number of substitutions that were made. repl
    can be either a string or a callable; if a string, backslash escapes in it
    are processed; if a callable, it's passed the match object and must return a
    replacement string to be used."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.subn(repl, string, count, pos, endpos, concurrent, timeout)

