
def primenu(n):
    r"""
    Calculate the number of distinct prime factors for a positive integer n.

    .. deprecated:: 1.13

        The ``primenu`` function is deprecated. Use :class:`sympy.functions.combinatorial.numbers.primenu`
        instead. See its documentation for more information. See
        :ref:`deprecated-ntheory-symbolic-functions` for details.

    If n's prime factorization is:

    .. math ::
        n = \prod_{i=1}^k p_i^{m_i},

    then ``primenu(n)`` or `\nu(n)` is:

    .. math ::
        \nu(n) = k.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import primenu
    >>> primenu(1)
    0
    >>> primenu(30)
    3

    See Also
    ========

    factorint

    References
    ==========

    .. [1] https://mathworld.wolfram.com/PrimeFactor.html

    """
    from sympy.functions.combinatorial.numbers import primenu as _primenu
    return _primenu(n)

