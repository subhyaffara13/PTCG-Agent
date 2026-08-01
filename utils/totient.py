
def totient(n):
    r"""
    Calculate the Euler totient function phi(n)

    .. deprecated:: 1.13

        The ``totient`` function is deprecated. Use :class:`sympy.functions.combinatorial.numbers.totient`
        instead. See its documentation for more information. See
        :ref:`deprecated-ntheory-symbolic-functions` for details.

    ``totient(n)`` or `\phi(n)` is the number of positive integers `\leq` n
    that are relatively prime to n.

    Parameters
    ==========

    n : integer

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import totient
    >>> totient(1)
    1
    >>> totient(25)
    20
    >>> totient(45) == totient(5)*totient(9)
    True

    See Also
    ========

    divisor_count

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Euler%27s_totient_function
    .. [2] https://mathworld.wolfram.com/TotientFunction.html

    """
    from sympy.functions.combinatorial.numbers import totient as _totient
    return _totient(n)


def totient(n):
    """Return the count of natural numbers up to *n* that are coprime with *n*.

    Euler's totient function φ(n) gives the number of totatives.
    Totative are integers k in the range 1 ≤ k ≤ n such that gcd(n, k) = 1.

    >>> n = 9
    >>> totient(n)
    6

    >>> totatives = [x for x in range(1, n) if gcd(n, x) == 1]
    >>> totatives
    [1, 2, 4, 5, 7, 8]
    >>> len(totatives)
    6

    Reference:  https://en.wikipedia.org/wiki/Euler%27s_totient_function

    """
    for prime in set(factor(n)):
        n -= n // prime
    return n

