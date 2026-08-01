
def _int0oo_1(g, x):
    r"""
    Evaluate $\int_0^\infty g\, dx$ using G functions,
    assuming the necessary conditions are fulfilled.

    Examples
    ========

    >>> from sympy.abc import a, b, c, d, x, y
    >>> from sympy import meijerg
    >>> from sympy.integrals.meijerint import _int0oo_1
    >>> _int0oo_1(meijerg([a], [b], [c], [d], x*y), x)
    gamma(-a)*gamma(c + 1)/(y*gamma(-d)*gamma(b + 1))
    """
    from sympy.simplify import gammasimp
    # See [L, section 5.6.1]. Note that s=1.
    eta, _ = _get_coeff_exp(g.argument, x)
    res = 1/eta
    # XXX TODO we should reduce order first
    for b in g.bm:
        res *= gamma(b + 1)
    for a in g.an:
        res *= gamma(1 - a - 1)
    for b in g.bother:
        res /= gamma(1 - b - 1)
    for a in g.aother:
        res /= gamma(a + 1)
    return gammasimp(unpolarify(res))

