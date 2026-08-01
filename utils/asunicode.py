
def asunicode(s):
    if isinstance(s, bytes):
        return s.decode('latin1')
    return str(s)

