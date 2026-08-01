
def rs_cos_sin(p, x, prec):
    """
    Cosine and sine of a series

    Return the series expansion of the cosine and sine of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_cos_sin
    >>> R, x, y = ring('x, y', QQ)
    >>> c, s = rs_cos_sin(x + x*y, x, 4)
    >>> c
    -1/2*x**2*y**2 - x**2*y - 1/2*x**2 + 1
    >>> s
    -1/6*x**3*y**3 - 1/2*x**3*y**2 - 1/2*x**3*y - 1/6*x**3 + x*y + x

    See Also
    ========

    rs_cos, rs_sin
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_cos_sin, p, x, prec)
    R = p.ring
    if not p:
        return R(0), R(0)
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            t1, t2 = R(sin(c_expr)), R(cos(c_expr))
        except ValueError:
            R = R.add_gens([sin(c_expr), cos(c_expr)])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            t1, t2 = R(sin(c_expr)), R(cos(c_expr))

        p1 = p - c
        p_cos, p_sin = rs_cos_sin(p1, x, prec)
        return p_cos*t2 - p_sin*t1, p_cos*t1 + p_sin*t2

    if len(p) > 20 and R.ngens == 1:
        t = rs_tan(p/2, x, prec)
        t2 = rs_square(t, x, prec)
        p1 = rs_series_inversion(1 + t2, x, prec)
        return (rs_mul(p1, 1 - t2, x, prec), rs_mul(p1, 2*t, x, prec))

    one = R(1)
    coeffs = []
    cn, sn = 1, 1
    for k in range(2, prec+2, 2):
        coeffs.extend([(one/cn, 0), (0, one/sn)])
        cn, sn = -cn*k*(k - 1), -sn*k*(k + 1)

    c, s = zip(*coeffs)
    return (rs_series_from_list(p, c, x, prec), rs_series_from_list(p, s, x, prec))

