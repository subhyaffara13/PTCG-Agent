
def _enhex(s):
    """Convert from binary string (bytes) to hex string (str)."""

    import binascii

    return bytestostr(binascii.hexlify(s))

