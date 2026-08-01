
def is_extra_strong_lucas_prp(n):
    """Extra Strong Lucas compositeness test.  Returns False if n is
    definitely composite, and True if n is an "extra strong" Lucas probable
    prime.

    The parameters are selected using P = 3, Q = 1, then incrementing P until
    (D|n) == -1.  The test itself is as defined in [1]_, from the
    Mo and Jones preprint.  The parameter selection and test are the same as
    used in OEIS A217719, Perl's Math::Prime::Util, and the Lucas pseudoprime
    page on Wikipedia.

    It is 20-50% faster than the strong test.

    Because of the different parameters selected, there is no relationship
    between the strong Lucas pseudoprimes and extra strong Lucas pseudoprimes.
    In particular, one is not a subset of the other.

    References
    ==========
    .. [1] Jon Grantham, Frobenius Pseudoprimes,
           Math. Comp. Vol 70, Number 234 (2001), pp. 873-891,
           https://doi.org/10.1090%2FS0025-5718-00-01197-2
    .. [2] OEIS A217719: Extra Strong Lucas Pseudoprimes
           https://oeis.org/A217719
    .. [3] https://en.wikipedia.org/wiki/Lucas_pseudoprime

    Examples
    ========

    >>> from sympy.ntheory.primetest import isprime, is_extra_strong_lucas_prp
    >>> for i in range(20000):
    ...     if is_extra_strong_lucas_prp(i) and not isprime(i):
    ...        print(i)
    989
    3239
    5777
    10877
    """
    # Implementation notes:
    #   1) the parameters differ from Thomas R. Nicely's.  His parameter
    #      selection leads to pseudoprimes that overlap M-R tests, and
    #      contradict Baillie and Wagstaff's suggestion of (D|n) = -1.
    #   2) The MathWorld page as of June 2013 specifies Q=-1.  The Lucas
    #      sequence must have Q=1.  See Grantham theorem 2.3, any of the
    #      references on the MathWorld page, or run it and see Q=-1 is wrong.
    n = as_int(n)
    if n == 2:
        return True
    if n < 2 or (n % 2) == 0:
        return False
    if gmpy_is_square(n):
        return False

    D, P, Q = _lucas_extrastrong_params(n)
    if D == 0:
        return False

    # remove powers of 2 from n+1 (= k * 2**s)
    s = bit_scan1(n + 1)
    k = (n + 1) >> s

    U, V, _ = _lucas_sequence(n, P, Q, k)

    if U == 0 and (V == 2 or V == n - 2):
        return True
    for _ in range(1, s):
        if V == 0:
            return True
        V = (V*V - 2) % n
    return False

