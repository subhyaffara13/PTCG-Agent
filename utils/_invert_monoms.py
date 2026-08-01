
def _invert_monoms(p1):
    """
    Compute ``x**n * p1(1/x)`` for a univariate polynomial ``p1`` in ``x``.

    Examples
    ========

    >>> from sympy.polys.domains import ZZ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import _invert_monoms
    >>> R, x = ring('x', ZZ)
    >>> p = x**2 + 2*x + 3
    >>> _invert_monoms(p)
    3*x**2 + 2*x + 1

    See Also
    ========

    sympy.polys.densebasic.dup_reverse
    """
    terms = list(p1.items())
    terms.sort()
    deg = p1.degree()
    R = p1.ring
    p = R.zero
    cv = p1.listcoeffs()
    mv = p1.listmonoms()
    for mvi, cvi in zip(mv, cv):
        p[(deg - mvi[0],)] = cvi
    return p

