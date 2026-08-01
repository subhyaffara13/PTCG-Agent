
def rs_tan(p, x, prec):
    """
    Tangent of a series.

    Return the series expansion of the tan of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_tan
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_tan(x + x*y, x, 4)
    1/3*x**3*y**3 + x**3*y**2 + x**3*y + 1/3*x**3 + x*y + x

   See Also
   ========

   _tan1, tan
   """
    if rs_is_puiseux(p, x):
        r = rs_puiseux(rs_tan, p, x, prec)
        return r
    R = p.ring
    const = 0
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            const = R(tan(c_expr))
        except ValueError:
            R = R.add_gens([tan(c_expr, )])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            const = R(tan(c_expr))

        p1 = p - c

    # Makes use of SymPy functions to evaluate the values of the cos/sin
    # of the constant term.
        t2 = rs_tan(p1, x, prec)
        t = rs_series_inversion(1 - const*t2, x, prec)
        return rs_mul(const + t2, t, x, prec)

    if R.ngens == 1:
        return _tan1(p, x, prec)
    else:
        return rs_fun(p, rs_tan, x, prec)

