
def as_text_type(s):
    if PY3 and isinstance(s, bytes):
        return s.decode('ascii')
    return s

