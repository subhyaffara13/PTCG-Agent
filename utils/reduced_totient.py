
def reduced_totient(n):
    r"""
    Calculate the Carmichael reduced totient function lambda(n)

    .. deprecated:: 1.13

        The ``reduced_totient`` function is deprecated. Use :class:`sympy.functions.combinatorial.numbers.reduced_totient`
        instead. See its documentation for more information. See
        :ref:`deprecated-ntheory-symbolic-functions` for details.

    ``reduced_totient(n)`` or `\lambda(n)` is the smallest m > 0 such that
    `k^m \equiv 1 \mod n` for all k relatively prime to n.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import reduced_totient
    >>> reduced_totient(1)
    1
    >>> reduced_totient(8)
    2
    >>> reduced_totient(30)
    4

    See Also
    ========

    totient

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Carmichael_function
    .. [2] https://mathworld.wolfram.com/CarmichaelFunction.html

    """
    from sympy.functions.combinatorial.numbers import reduced_totient as _reduced_totient
    return _reduced_totient(n)

