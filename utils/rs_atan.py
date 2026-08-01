
def rs_atan(p, x, prec):
    """
    The arctangent of a series

    Return the series expansion of the atan of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_atan
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_atan(x + x*y, x, 4)
    -1/3*x**3*y**3 - x**3*y**2 - x**3*y - 1/3*x**3 + x*y + x

    See Also
    ========

    atan
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_atan, p, x, prec)
    R = p.ring
    const = 0
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            const = R(atan(c_expr))
        except ValueError:
            R = R.add_gens([atan(c_expr)])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            const = R(atan(c_expr))

    # Instead of using a closed form formula, we differentiate atan(p) to get
    # `1/(1+p**2) * dp`, whose series expansion is much easier to calculate.
    # Finally we integrate to get back atan
    dp = p.diff(x)
    p1 = rs_square(p, x, prec) + R(1)
    p1 = rs_series_inversion(p1, x, prec - 1)
    p1 = rs_mul(dp, p1, x, prec - 1)
    return rs_integrate(p1, x) + const

