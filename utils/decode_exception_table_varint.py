
def decode_exception_table_varint(bytes_iter: Iterator[int]) -> int:
    """
    Inverse of `encode_exception_table_varint`.
    """
    b = next(bytes_iter)
    val = b & 63
    while b & 64:
        val <<= 6
        b = next(bytes_iter)
        val |= b & 63
    return val

