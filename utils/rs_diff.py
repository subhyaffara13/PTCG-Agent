
def rs_diff(p, x):
    """
    Return partial derivative of ``p`` with respect to ``x``.

    Parameters
    ==========

    x : :class:`~.PolyElement` with respect to which ``p`` is differentiated.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_diff
    >>> R, x, y = ring('x, y', QQ)
    >>> p = x + x**2*y**3
    >>> rs_diff(p, x)
    2*x*y**3 + 1
    """
    R = p.ring
    n = R.gens.index(x)
    p1 = {}
    mn = [0]*R.ngens
    mn[n] = 1
    mn = tuple(mn)
    for expv in p:
        if expv[n]:
            e = monomial_ldiv(expv, mn)
            p1[e] = R.domain_new(p[expv]*expv[n])
    return R(p1)

