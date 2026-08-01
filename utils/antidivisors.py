
def antidivisors(n, generator=False):
    r"""
    Return all antidivisors of n sorted from 1..n by default.

    Antidivisors [1]_ of n are numbers that do not divide n by the largest
    possible margin.  If generator is True an unordered generator is returned.

    Examples
    ========

    >>> from sympy.ntheory.factor_ import antidivisors
    >>> antidivisors(24)
    [7, 16]

    >>> sorted(antidivisors(128, generator=True))
    [3, 5, 15, 17, 51, 85]

    See Also
    ========

    primefactors, factorint, divisors, divisor_count, antidivisor_count

    References
    ==========

    .. [1] definition is described in https://oeis.org/A066272/a066272a.html

    """
    rv = _antidivisors(as_int(abs(n)))
    return rv if generator else sorted(rv)

