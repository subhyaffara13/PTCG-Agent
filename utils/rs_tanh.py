
def rs_tanh(p, x, prec):
    """
    Hyperbolic tangent of a series

    Return the series expansion of the tanh of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_tanh
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_tanh(x + x*y, x, 4)
    -1/3*x**3*y**3 - x**3*y**2 - x**3*y - 1/3*x**3 + x*y + x

    See Also
    ========

    tanh
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_tanh, p, x, prec)
    R = p.ring
    const = 0
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            const = R(tanh(c_expr))
        except ValueError:
            R = R.add_gens([tanh(c_expr)])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            const = R(tanh(c_expr))

        p1 = p - c
        t1 = rs_tanh(p1, x, prec)
        t = rs_series_inversion(1 + const*t1, x, prec)
        return rs_mul(const + t1, t, x, prec)

    if R.ngens == 1:
        return _tanh(p, x, prec)
    else:
        return rs_fun(p, _tanh, x, prec)

