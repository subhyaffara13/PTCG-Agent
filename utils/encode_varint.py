
def encode_varint(n: int) -> list[int]:
    """
    6-bit chunk encoding of an unsigned integer
    See https://github.com/python/cpython/blob/3.11/Objects/locations.md
    """
    assert n >= 0
    b = [n & 63]
    n >>= 6
    while n > 0:
        b[-1] |= 64
        b.append(n & 63)
        n >>= 6
    return b

