
def splititer(pattern, string, maxsplit=0, flags=0, concurrent=None,
  timeout=None, ignore_unused=False, **kwargs):
    "Return an iterator yielding the parts of a split string."
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.splititer(string, maxsplit, concurrent, timeout)

