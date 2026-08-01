
def rs_integrate(p, x):
    """
    Integrate ``p`` with respect to ``x``.

    Parameters
    ==========

    x : :class:`~.PolyElement` with respect to which ``p`` is integrated.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_integrate
    >>> R, x, y = ring('x, y', QQ)
    >>> p = x + x**2*y**3
    >>> rs_integrate(p, x)
    1/3*x**3*y**3 + 1/2*x**2
    """
    R = p.ring
    p1 = {}
    n = R.gens.index(x)
    mn = [0]*R.ngens
    mn[n] = 1
    mn = tuple(mn)

    for expv in p:
        e = monomial_mul(expv, mn)
        p1[e] = R.domain_new(p[expv]/(expv[n] + 1))
    return R(p1)

