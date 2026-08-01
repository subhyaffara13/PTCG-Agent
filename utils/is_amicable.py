
def is_amicable(m, n):
    """Returns True if the numbers `m` and `n` are "amicable", else False.

    Amicable numbers are two different numbers so related that the sum
    of the proper divisors of each is equal to that of the other.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import divisor_sigma
    >>> from sympy.ntheory.factor_ import is_amicable
    >>> is_amicable(220, 284)
    True
    >>> divisor_sigma(220) == divisor_sigma(284)
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Amicable_numbers

    """
    return m != n and m + n == _divisor_sigma(m) == _divisor_sigma(n)

