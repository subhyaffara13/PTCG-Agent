
def proth_test(n):
    r""" Test if the Proth number `n = k2^m + 1` is prime. where k is a positive odd number and `2^m > k`.

    Parameters
    ==========

    n : Integer
        ``n`` is Proth number

    Returns
    =======

    bool : If ``True``, then ``n`` is the Proth prime

    Raises
    ======

    ValueError
        If ``n`` is not Proth number.

    Examples
    ========

    >>> from sympy.ntheory.primetest import proth_test
    >>> proth_test(41)
    True
    >>> proth_test(57)
    False

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Proth_prime

    """
    n = as_int(n)
    if n < 3:
        raise ValueError("n is not Proth number")
    m = bit_scan1(n - 1)
    k = n >> m
    if m < k.bit_length():
        raise ValueError("n is not Proth number")
    if n % 3 == 0:
        return n == 3
    if k % 3: # n % 12 == 5
        return pow(3, n >> 1, n) == n - 1
    # If `n` is a square number, then `jacobi(a, n) = 1` for any `a`
    if gmpy_is_square(n):
        return False
    # `a` may be chosen at random.
    # In any case, we want to find `a` such that `jacobi(a, n) = -1`.
    for a in range(5, n):
        j = jacobi(a, n)
        if j == -1:
            return pow(a, n >> 1, n) == n - 1
        if j == 0:
            return False

