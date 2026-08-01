
def is_combining(sym):
    """Check whether symbol is a unicode modifier. """

    return ord(sym) in _remove_combining

