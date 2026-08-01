
def sieve(n):
    """Yield the primes less than n.

    >>> list(sieve(30))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    """
    # This implementation comes from an older version of the itertools
    # documentation.  The newer implementation is easier to read but is
    # less lazy.
    if n > 2:
        yield 2
    start = 3
    data = bytearray((0, 1)) * (n // 2)
    for p in iter_index(data, 1, start, stop=isqrt(n) + 1):
        yield from iter_index(data, 1, start, p * p)
        data[p * p : n : p + p] = bytes(len(range(p * p, n, p + p)))
        start = p * p
    yield from iter_index(data, 1, start)

