
def is_strong_lucas_prp(n, p, q):
    D = p**2 - 4*q
    if D == 0:
        raise ValueError("invalid values for p,q in is_strong_lucas_prp()")
    if n < 1:
        raise ValueError("is_selfridge_prp() requires 'n' be greater than 0")
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    if gcd(n, q*D) not in [1, n]:
        raise ValueError("is_strong_lucas_prp() requires gcd(n,2*q*D) == 1")
    j = jacobi(D, n)
    s = bit_scan1(n - j)
    U, V, Qk = _lucas_sequence(n, p, q, (n - j) >> s)
    if U == 0 or V == 0:
        return True
    for _ in range(s - 1):
        V = (V*V - 2*Qk) % n
        if V == 0:
            return True
        Qk = pow(Qk, 2, n)
    return False


def is_strong_lucas_prp(n):
    """Strong Lucas compositeness test with Selfridge parameters.  Returns
    False if n is definitely composite, and True if n is a strong Lucas
    probable prime.

    This is often used in combination with the Miller-Rabin test, and
    in particular, when combined with M-R base 2 creates the strong BPSW test.

    References
    ==========
    .. [1] Robert Baillie, Samuel S. Wagstaff, Lucas Pseudoprimes,
           Math. Comp. Vol 35, Number 152 (1980), pp. 1391-1417,
           https://doi.org/10.1090%2FS0025-5718-1980-0583518-6
           http://mpqs.free.fr/LucasPseudoprimes.pdf
    .. [2] OEIS A217255: Strong Lucas Pseudoprimes
           https://oeis.org/A217255
    .. [3] https://en.wikipedia.org/wiki/Lucas_pseudoprime
    .. [4] https://en.wikipedia.org/wiki/Baillie-PSW_primality_test

    Examples
    ========

    >>> from sympy.ntheory.primetest import isprime, is_strong_lucas_prp
    >>> for i in range(20000):
    ...     if is_strong_lucas_prp(i) and not isprime(i):
    ...        print(i)
    5459
    5777
    10877
    16109
    18971
    """
    n = as_int(n)
    if n < 2:
        return False
    return is_strong_selfridge_prp(n)

