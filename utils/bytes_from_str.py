
def bytes_from_str(value: str) -> bytes:
    """Convert a string representing bytes into actual bytes.

    This is needed because the literal characters of BytesExpr (the
    characters inside b'') are stored in BytesExpr.value, whose type is
    'str' not 'bytes'.
    """
    return bytes(value, "utf8").decode("unicode-escape").encode("raw-unicode-escape")

