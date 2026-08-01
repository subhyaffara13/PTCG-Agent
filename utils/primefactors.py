
def primefactors(n, limit=None, verbose=False, **kwargs):
    """Return a sorted list of n's prime factors, ignoring multiplicity
    and any composite factor that remains if the limit was set too low
    for complete factorization. Unlike factorint(), primefactors() does
    not return -1 or 0.

    Parameters
    ==========

    n : integer
    limit, verbose, **kwargs :
        Additional keyword arguments to be passed to ``factorint``.
        Since ``kwargs`` is new in version 1.13,
        ``limit`` and ``verbose`` are retained for compatibility purposes.

    Returns
    =======

    list(int) : List of prime numbers dividing ``n``

    Examples
    ========

    >>> from sympy.ntheory import primefactors, factorint, isprime
    >>> primefactors(6)
    [2, 3]
    >>> primefactors(-5)
    [5]

    >>> sorted(factorint(123456).items())
    [(2, 6), (3, 1), (643, 1)]
    >>> primefactors(123456)
    [2, 3, 643]

    >>> sorted(factorint(10000000001, limit=200).items())
    [(101, 1), (99009901, 1)]
    >>> isprime(99009901)
    False
    >>> primefactors(10000000001, limit=300)
    [101]

    See Also
    ========

    factorint, divisors

    """
    n = int(n)
    kwargs.update({"visual": None, "multiple": False,
                   "limit": limit, "verbose": verbose})
    factors = sorted(factorint(n=n, **kwargs).keys())
    # We want to calculate
    # s = [f for f in factors if isprime(f)]
    s = [f for f in factors[:-1:] if f not in [-1, 0, 1]]
    if factors and isprime(factors[-1]):
        s += [factors[-1]]
    return s

