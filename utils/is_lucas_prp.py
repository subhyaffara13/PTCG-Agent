
def is_lucas_prp(n, p, q):
    d = p**2 - 4*q
    if d == 0:
        raise ValueError("invalid values for p,q in is_lucas_prp()")
    if n < 1:
        raise ValueError("is_lucas_prp() requires 'n' be greater than 0")
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    if gcd(n, q*d) not in [1, n]:
        raise ValueError("is_lucas_prp() requires gcd(n,2*q*D) == 1")
    return _lucas_sequence(n, p, q, n - jacobi(d, n))[0] == 0


def is_lucas_prp(n):
    """Standard Lucas compositeness test with Selfridge parameters.  Returns
    False if n is definitely composite, and True if n is a Lucas probable
    prime.

    This is typically used in combination with the Miller-Rabin test.

    References
    ==========
    .. [1] Robert Baillie, Samuel S. Wagstaff, Lucas Pseudoprimes,
           Math. Comp. Vol 35, Number 152 (1980), pp. 1391-1417,
           https://doi.org/10.1090%2FS0025-5718-1980-0583518-6
           http://mpqs.free.fr/LucasPseudoprimes.pdf
    .. [2] OEIS A217120: Lucas Pseudoprimes
           https://oeis.org/A217120
    .. [3] https://en.wikipedia.org/wiki/Lucas_pseudoprime

    Examples
    ========

    >>> from sympy.ntheory.primetest import isprime, is_lucas_prp
    >>> for i in range(10000):
    ...     if is_lucas_prp(i) and not isprime(i):
    ...         print(i)
    323
    377
    1159
    1829
    3827
    5459
    5777
    9071
    9179
    """
    n = as_int(n)
    if n < 2:
        return False
    return is_selfridge_prp(n)

