
def format_int(n: int) -> bytes:
    """Format an integer using a variable-length binary encoding."""
    if n < 128:
        a = [n]
    else:
        a = []
        while n > 0:
            a.insert(0, n & 0x7F)
            n >>= 7
        for i in range(len(a) - 1):
            # If the highest bit is set, more 7-bit digits follow
            a[i] |= 0x80
    return bytes(a)

