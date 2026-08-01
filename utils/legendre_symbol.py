
def legendre_symbol(a, p):
    r"""
    Returns the Legendre symbol `(a / p)`.

    .. deprecated:: 1.13

        The ``legendre_symbol`` function is deprecated. Use :class:`sympy.functions.combinatorial.numbers.legendre_symbol`
        instead. See its documentation for more information. See
        :ref:`deprecated-ntheory-symbolic-functions` for details.

    For an integer ``a`` and an odd prime ``p``, the Legendre symbol is
    defined as

    .. math ::
        \genfrac(){}{}{a}{p} = \begin{cases}
             0 & \text{if } p \text{ divides } a\\
             1 & \text{if } a \text{ is a quadratic residue modulo } p\\
            -1 & \text{if } a \text{ is a quadratic nonresidue modulo } p
        \end{cases}

    Parameters
    ==========

    a : integer
    p : odd prime

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import legendre_symbol
    >>> [legendre_symbol(i, 7) for i in range(7)]
    [0, 1, 1, -1, 1, -1, -1]
    >>> sorted(set([i**2 % 7 for i in range(7)]))
    [0, 1, 2, 4]

    See Also
    ========

    is_quad_residue, jacobi_symbol

    """
    from sympy.functions.combinatorial.numbers import legendre_symbol as _legendre_symbol
    return _legendre_symbol(a, p)

