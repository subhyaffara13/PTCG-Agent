
def rs_cos(p, x, prec):
    """
    Cosine of a series

    Return the series expansion of the cos of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.puiseux import puiseux_ring
    >>> from sympy.polys.ring_series import rs_cos
    >>> R, x, y = puiseux_ring('x, y', QQ)
    >>> rs_cos(x + x*y, x, 4)
    1 + -1/2*x**2 + -1*x**2*y + -1/2*x**2*y**2
    >>> rs_cos(x + x*y, x, 4)/x**QQ(7, 5)
    x**(-7/5) + -1/2*x**(3/5) + -1*x**(3/5)*y + -1/2*x**(3/5)*y**2

    See Also
    ========

    cos
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_cos, p, x, prec)
    R = p.ring
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
        # Makes use of SymPy cos, sin functions to evaluate the values of the
        # cos/sin of the constant term.
        p_cos, p_sin = rs_cos_sin(p1, x, prec)
        return p_cos*t2 - p_sin*t1

    # Series is calculated in terms of tan as its evaluation is fast.
    if len(p) > 20 and R.ngens == 1:
        t = rs_tan(p/2, x, prec)
        t2 = rs_square(t, x, prec)
        p1 = rs_series_inversion(1+t2, x, prec)
        return rs_mul(p1, 1 - t2, x, prec)
    one = R(1)
    n = 1
    c = []
    for k in range(2, prec + 2, 2):
        c.append(one/n)
        c.append(0)
        n *= -k*(k - 1)
    return rs_series_from_list(p, c, x, prec)

