
def _sanitize_message(thing):
    s = str(thing)
    s = _sanitize_general(s)
    return _hexadecimal.sub("0", s)

