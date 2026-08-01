
def _lucas_lehmer_primality_test(p):
    r""" Test if the Mersenne number `M_p = 2^p-1` is prime.

    Parameters
    ==========

    p : int
        ``p`` is an odd prime number

    Returns
    =======

    bool : If ``True``, then `M_p` is the Mersenne prime

    Examples
    ========

    >>> from sympy.ntheory.primetest import _lucas_lehmer_primality_test
    >>> _lucas_lehmer_primality_test(5) # 2**5 - 1 = 31 is prime
    True
    >>> _lucas_lehmer_primality_test(11) # 2**11 - 1 = 2047 is not prime
    False

    See Also
    ========

    is_mersenne_prime

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test

    """
    v = 4
    m = 2**p - 1
    for _ in range(p - 2):
        v = pow(v, 2, m) - 2
    return v == 0

