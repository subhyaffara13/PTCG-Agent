
def c_string_initializer(value: bytes) -> str:
    """Create initializer for a C char[]/ char * variable from a string.

    For example, if value if b'foo', the result would be '"foo"'.
    """
    return '"' + encode_bytes_as_c_string(value) + '"'

