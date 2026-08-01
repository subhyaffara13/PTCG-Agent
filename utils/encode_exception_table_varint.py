
def encode_exception_table_varint(n: int) -> list[int]:
    """
    Similar to `encode_varint`, but the 6-bit chunks are ordered in reverse.
    """
    assert n >= 0
    b = [n & 63]
    n >>= 6
    while n > 0:
        b.append(n & 63)
        n >>= 6
    b.reverse()
    for i in range(len(b) - 1):
        b[i] |= 64
    return b

