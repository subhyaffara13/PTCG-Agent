
def rs_cosh(p, x, prec):
    """
    Hyperbolic cosine of a series

    Return the series expansion of the cosh of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_cosh
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_cosh(x + x*y, x, 4)
    1/2*x**2*y**2 + x**2*y + 1/2*x**2 + 1

    See Also
    ========

    cosh
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_cosh, p, x, prec)
    R = p.ring
    if not p:
        return R(0)
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            t1, t2 = R(sinh(c_expr)), R(cosh(c_expr))
        except ValueError:
            R = R.add_gens([sinh(c_expr), cosh(c_expr)])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            t1, t2 = R(sinh(c_expr)), R(cosh(c_expr))

        p1 = p - c
        p_cosh, p_sinh = rs_cosh_sinh(p1, x, prec)
        return p_cosh * t2 + p_sinh * t1

    t = rs_exp(p, x, prec)
    t1 = rs_series_inversion(t, x, prec)
    return (t + t1)/2

