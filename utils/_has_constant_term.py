
def _has_constant_term(p, x):
    """
    Check if ``p`` has a constant term in ``x``

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import _has_constant_term
    >>> R, x = ring('x', QQ)
    >>> p = x**2 + x + 1
    >>> _has_constant_term(p, x)
    True
    """
    R = p.ring
    iv = R.gens.index(x)
    zm = R.zero_monom
    a = [0]*R.ngens
    a[iv] = 1
    miv = tuple(a)
    return any(monomial_min(expv, miv) == zm for expv in p)

