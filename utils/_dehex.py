
def _dehex(s):
    """Liberally convert from hex string to binary string."""
    import re
    import binascii

    # Remove all non-hexadecimal digits
    s = re.sub(r"[^a-fA-F\d]", "", s)
    # binscii.unhexlify works in Python 2 and Python 3 (unlike
    # thing.decode('hex')).
    return binascii.unhexlify(strtobytes(s))

