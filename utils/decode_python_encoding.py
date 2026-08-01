
def decode_python_encoding(source: bytes) -> str:
    """Read the Python file with while obeying PEP-263 encoding detection.

    Returns the source as a string.
    """
    # check for BOM UTF-8 encoding and strip it out if present
    if source.startswith(b"\xef\xbb\xbf"):
        encoding = "utf8"
        source = source[3:]
    else:
        # look at first two lines and check if PEP-263 coding is present
        encoding, _ = find_python_encoding(source)

    try:
        source_text = source.decode(encoding)
    except LookupError as lookuperr:
        raise DecodeError(str(lookuperr)) from lookuperr
    return source_text

