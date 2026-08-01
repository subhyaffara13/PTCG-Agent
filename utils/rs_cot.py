
def rs_cot(p, x, prec):
    """
    Cotangent of a series

    Return the series expansion of the cot of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_cot
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_cot(x, x, 6)
    -2/945*x**5 - 1/45*x**3 - 1/3*x + x**(-1)

    See Also
    ========

    cot
    """
    # It can not handle series like `p = x + x*y` where the coefficient of the
    # linear term in the series variable is symbolic.
    if rs_is_puiseux(p, x):
        r = rs_puiseux(rs_cot, p, x, prec)
        return r
    i, m = _check_series_var(p, x, 'cot')
    prec1 = int(prec + 2*m)
    c, s = rs_cos_sin(p, x, prec1)
    s = mul_xin(s, i, -m)
    s = rs_series_inversion(s, x, prec1)
    res = rs_mul(c, s, x, prec1)
    res = mul_xin(res, i, -m)
    res = rs_trunc(res, x, prec)
    return res

