
def bytes_to_human_readable_repr(b: bytes) -> str:
    """Converts bytes into some human-readable representation. Unprintable
    bytes such as the nul byte are escaped. For example:

        >>> b = bytes([102, 111, 111, 10, 0])
        >>> s = bytes_to_human_readable_repr(b)
        >>> print(s)
        foo\n\x00
        >>> print(repr(s))
        'foo\\n\\x00'
    """
    return repr(b)[2:-1]

