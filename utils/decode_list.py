
def decode_list(b):
    """
    Given a non-deserializable object, make a best effort to
    return a useful set of results.
    """
    if isinstance(b, list):
        return [nativestr(obj) for obj in b]
    elif isinstance(b, bytes):
        return unstring(nativestr(b))
    elif isinstance(b, str):
        return unstring(b)
    return b

