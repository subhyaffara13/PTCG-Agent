
def isqrt_small_python(x):
    """
    Correctly (floor) rounded integer square root, using
    division. Fast up to ~200 digits.
    """
    if not x:
        return x
    if x < _1_800:
        # Exact with IEEE double precision arithmetic
        if x < _1_50:
            return int(x**0.5)
        # Initial estimate can be any integer >= the true root; round up
        r = int(x**0.5 * 1.00000000000001) + 1
    else:
        bc = bitcount(x)
        n = bc//2
        r = int((x>>(2*n-100))**0.5+2)<<(n-50)  # +2 is to round up
    # The following iteration now precisely computes floor(sqrt(x))
    # See e.g. Crandall & Pomerance, "Prime Numbers: A Computational
    # Perspective"
    while 1:
        y = (r+x//r)>>1
        if y >= r:
            return r
        r = y

