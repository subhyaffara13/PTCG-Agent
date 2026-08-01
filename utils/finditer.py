
def finditer(pattern, string, flags=0, pos=None, endpos=None, overlapped=False,
  partial=False, concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Return an iterator over all matches in the string. The matches may be
    overlapped if overlapped is True. For each match, the iterator returns a
    match object. Empty matches are included in the result."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.finditer(string, pos, endpos, overlapped, concurrent, partial,
      timeout)

