
def stn(s, length, encoding, errors):
    """Convert a string to a null-terminated bytes object.
    """
    if s is None:
        raise ValueError("metadata cannot contain None")
    s = s.encode(encoding, errors)
    return s[:length] + (length - len(s)) * NUL

