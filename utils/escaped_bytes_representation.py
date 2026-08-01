
def escaped_bytes_representation(b):
    """PY3 bytes need escaping for comparison with other strings.

    In practice it turns control characters into acceptable codepoints then
    encodes them into bytes again to turn unprintable bytes into printable
    escape sequences.

    This is safe to do for the whole range 0..255 and result matches
    unicode_escape on a unicode string.
    """
    return b.decode("unicode_escape").encode("unicode_escape")

