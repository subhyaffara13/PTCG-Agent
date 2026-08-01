
def _sanitize(s):
    return _INVALID_GRAPHITE_CHARS.sub('_', s)

