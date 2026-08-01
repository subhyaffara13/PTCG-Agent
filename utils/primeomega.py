
def primeomega(n):
    r"""
    Calculate the number of prime factors counting multiplicities for a
    positive integer n.

    .. deprecated:: 1.13

        The ``primeomega`` function is deprecated. Use :class:`sympy.functions.combinatorial.numbers.primeomega`
        instead. See its documentation for more information. See
        :ref:`deprecated-ntheory-symbolic-functions` for details.

    If n's prime factorization is:

    .. math ::
        n = \prod_{i=1}^k p_i^{m_i},

    then ``primeomega(n)``  or `\Omega(n)` is:

    .. math ::
        \Omega(n) = \sum_{i=1}^k m_i.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import primeomega
    >>> primeomega(1)
    0
    >>> primeomega(20)
    3

    See Also
    ========

    factorint

    References
    ==========

    .. [1] https://mathworld.wolfram.com/PrimeFactor.html

    """
    from sympy.functions.combinatorial.numbers import primeomega as _primeomega
    return _primeomega(n)

