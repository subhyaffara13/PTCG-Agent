
def _clean_repr(obj):
  return _ADDR_RE.sub(r'<\1>', repr(obj))

