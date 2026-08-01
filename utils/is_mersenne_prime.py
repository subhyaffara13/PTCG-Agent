
def is_mersenne_prime(n):
    """Returns True if  ``n`` is a Mersenne prime, else False.

    A Mersenne prime is a prime number having the form `2^i - 1`.

    Examples
    ========

    >>> from sympy.ntheory.factor_ import is_mersenne_prime
    >>> is_mersenne_prime(6)
    False
    >>> is_mersenne_prime(127)
    True

    References
    ==========

    .. [1] https://mathworld.wolfram.com/MersennePrime.html

    """
    n = as_int(n)
    if n < 1:
        return False
    if n & (n + 1):
        # n is not Mersenne number
        return False
    p = n.bit_length()
    if p in MERSENNE_PRIME_EXPONENTS:
        return True
    if p < 65_000_000 or not isprime(p):
        # According to GIMPS, verification was completed on September 19, 2023 for p less than 65 million.
        # https://www.mersenne.org/report_milestones/
        # If p is composite number, then n=2**p-1 is composite number.
        return False
    result = _lucas_lehmer_primality_test(p)
    if result:
        raise ValueError(filldedent('''
            This Mersenne Prime, 2^%s - 1, should
            be added to SymPy's known values.''' % p))
    return result

