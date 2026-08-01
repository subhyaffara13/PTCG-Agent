
def base128Size(n):
    """Return the length in bytes of a UIntBase128-encoded sequence with value n.

    >>> base128Size(0)
    1
    >>> base128Size(24567)
    3
    >>> base128Size(2**32-1)
    5
    """
    assert n >= 0
    size = 1
    while n >= 128:
        size += 1
        n >>= 7
    return size

