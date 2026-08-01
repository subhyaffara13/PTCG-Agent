
def python_trailing(n):
    """Count the number of trailing zero bits in abs(n)."""
    if not n:
        return 0
    low_byte = n & 0xff
    if low_byte:
        return small_trailing[low_byte]
    t = 8
    n >>= 8
    while not n & 0xff:
        n >>= 8
        t += 8
    return t + small_trailing[n & 0xff]

