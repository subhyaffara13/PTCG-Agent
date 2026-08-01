
def divisor_count(n, modulus=1, proper=False):
    """
    Return the number of divisors of ``n``. If ``modulus`` is not 1 then only
    those that are divisible by ``modulus`` are counted. If ``proper`` is True
    then the divisor of ``n`` will not be counted.

    Examples
    ========

    >>> from sympy import divisor_count
    >>> divisor_count(6)
    4
    >>> divisor_count(6, 2)
    2
    >>> divisor_count(6, proper=True)
    3

    See Also
    ========

    factorint, divisors, totient, proper_divisor_count

    """

    if not modulus:
        return 0
    elif modulus != 1:
        n, r = divmod(n, modulus)
        if r:
            return 0
    if n == 0:
        return 0
    n = Mul(*[v + 1 for k, v in factorint(n).items() if k > 1])
    if n and proper:
        n -= 1
    return n

