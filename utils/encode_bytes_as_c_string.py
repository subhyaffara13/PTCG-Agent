
def encode_bytes_as_c_string(b: bytes) -> str:
    """Produce contents of a C string literal for a byte string, without quotes."""
    escaped = "".join([CHAR_MAP[i] for i in b])
    return escaped

