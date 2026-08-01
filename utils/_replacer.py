
def _replacer(data, value):
    """
    Either returns ``data[value]`` or passes ``data`` back, converting any
    ``MappingView`` to a sequence.
    """
    try:
        # if key isn't a string don't bother
        if isinstance(value, str):
            # try to use __getitem__
            value = data[value]
    except Exception:
        # key does not exist, silently fall back to key
        pass
    return cbook.sanitize_sequence(value)


def _replacer(x) -> str:
    """
    Replace a number with its hexadecimal representation. Used to tag
    temporary variables with their calling scope's id.
    """
    # get the hex repr of the binary char and remove 0x and pad by pad_size
    # zeros
    try:
        hexin = ord(x)
    except TypeError:
        # bytes literals masquerade as ints when iterating in py3
        hexin = x

    return hex(hexin)

