
def multiplicity_in_factorial(p, n):
    """return the largest integer ``m`` such that ``p**m`` divides ``n!``
    without calculating the factorial of ``n``.

    Parameters
    ==========

    p : Integer
        positive integer
    n : Integer
        non-negative integer

    Examples
    ========

    >>> from sympy.ntheory import multiplicity_in_factorial
    >>> from sympy import factorial

    >>> multiplicity_in_factorial(2, 3)
    1

    An instructive use of this is to tell how many trailing zeros
    a given factorial has. For example, there are 6 in 25!:

    >>> factorial(25)
    15511210043330985984000000
    >>> multiplicity_in_factorial(10, 25)
    6

    For large factorials, it is much faster/feasible to use
    this function rather than computing the actual factorial:

    >>> multiplicity_in_factorial(factorial(25), 2**100)
    52818775009509558395695966887

    See Also
    ========

    multiplicity

    """

    p, n = as_int(p), as_int(n)

    if p <= 0:
        raise ValueError('expecting positive integer got %s' % p )

    if n < 0:
        raise ValueError('expecting non-negative integer got %s' % n )

    # keep only the largest of a given multiplicity since those
    # of a given multiplicity will be goverened by the behavior
    # of the largest factor
    f = defaultdict(int)
    for k, v in factorint(p).items():
        f[v] = max(k, f[v])
    # multiplicity of p in n! depends on multiplicity
    # of prime `k` in p, so we floor divide by `v`
    # and keep it if smaller than the multiplicity of p
    # seen so far
    return min((n + k - sum(digits(n, k)))//(k - 1)//v for v, k in f.items())

