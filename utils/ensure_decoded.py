
def ensure_decoded(s) -> str:
    """
    If we have bytes, decode them to unicode.
    """
    if isinstance(s, (np.bytes_, bytes)):
        s = s.decode(get_option("display.encoding"))
    return s

