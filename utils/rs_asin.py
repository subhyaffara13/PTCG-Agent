
def rs_asin(p, x, prec):
    """
    Arcsine of a series

    Return the series expansion of the asin of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_asin
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_asin(x, x, 8)
    5/112*x**7 + 3/40*x**5 + 1/6*x**3 + x

    See Also
    ========

    asin
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_asin, p, x, prec)
    if _has_constant_term(p, x):
        raise NotImplementedError("Polynomial must not have constant term in "
                                    "series variables")
    R = p.ring
    if x in R.gens:
        # get a good value
        if len(p) > 20:
            dp = rs_diff(p, x)
            p1 = 1 - rs_square(p, x, prec - 1)
            p1 = rs_nth_root(p1, -2, x, prec - 1)
            p1 = rs_mul(dp, p1, x, prec - 1)
            return rs_integrate(p1, x)
        one = R(1)
        c = [0, one, 0]
        for k in range(3, prec, 2):
            c.append((k - 2)**2*c[-2]/(k*(k - 1)))
            c.append(0)
        return rs_series_from_list(p, c, x, prec)

    else:
        raise NotImplementedError

