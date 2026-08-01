
def rs_atanh(p, x, prec):
    """
    Hyperbolic arctangent of a series

    Return the series expansion of the atanh of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_atanh
    >>> R, x, y = ring('x, y', QQ)
    >>> rs_atanh(x + x*y, x, 4)
    1/3*x**3*y**3 + x**3*y**2 + x**3*y + 1/3*x**3 + x*y + x

    See Also
    ========

    atanh
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_atanh, p, x, prec)
    R = p.ring
    const = 0
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            const = R(atanh(c_expr))
        except ValueError:
            raise DomainError("The given series cannot be expanded in "
                "this domain.")

    # Instead of using a closed form formula, we differentiate atanh(p) to get
    # `1/(1-p**2) * dp`, whose series expansion is much easier to calculate.
    # Finally we integrate to get back atanh
    dp = rs_diff(p, x)
    p1 = - rs_square(p, x, prec) + 1
    p1 = rs_series_inversion(p1, x, prec - 1)
    p1 = rs_mul(dp, p1, x, prec - 1)
    return rs_integrate(p1, x) + const

