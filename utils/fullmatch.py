
def fullmatch(pattern, string, flags=0, pos=None, endpos=None, partial=False,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Try to apply the pattern against all of the string, returning a match
    object, or None if no match was found."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.fullmatch(string, pos, endpos, concurrent, partial, timeout)

