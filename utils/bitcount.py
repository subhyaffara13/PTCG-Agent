
def bitcount(n):
    """Return smallest integer, b, such that |n|/2**b < 1.
    """
    return mpmath_bitcount(abs(int(n)))

