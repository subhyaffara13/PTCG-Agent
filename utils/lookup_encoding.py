
def lookupEncoding(encoding):
    """Return the python codec name corresponding to an encoding or None if the
    string doesn't correspond to a valid encoding."""
    if isinstance(encoding, bytes):
        try:
            encoding = encoding.decode("ascii")
        except UnicodeDecodeError:
            return None

    if encoding is not None:
        try:
            return webencodings.lookup(encoding)
        except AttributeError:
            return None
    else:
        return None

