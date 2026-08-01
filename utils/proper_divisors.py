
def proper_divisors(n, generator=False):
    """
    Return all divisors of n except n, sorted by default.
    If generator is ``True`` an unordered generator is returned.

    Examples
    ========

    >>> from sympy import proper_divisors, proper_divisor_count
    >>> proper_divisors(24)
    [1, 2, 3, 4, 6, 8, 12]
    >>> proper_divisor_count(24)
    7
    >>> list(proper_divisors(120, generator=True))
    [1, 2, 4, 8, 3, 6, 12, 24, 5, 10, 20, 40, 15, 30, 60]

    See Also
    ========

    factorint, divisors, proper_divisor_count

    """
    return divisors(n, generator=generator, proper=True)

