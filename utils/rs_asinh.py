
def rs_asinh(p, x, prec):
    """
    Hyperbolic arcsine of a series

    Return the series expansion of the arcsinh of ``p``, about 0.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_asinh
    >>> R, x = ring('x', QQ)
    >>> rs_asinh(x, x, 9)
    -5/112*x**7 + 3/40*x**5 - 1/6*x**3 + x

    See Also
    ========

    asinh
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_asinh, p, x, prec)
    R = p.ring
    const = 0
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            const = R(asinh(c_expr))
        except ValueError:
            raise DomainError("The given series cannot be expanded in "
                "this domain.")

    # Instead of using a closed form formula, we differentiate asinh(p) to get
    # `1/sqrt(1+p**2) * dp`, whose series expansion is much easier to calculate.
    # Finally we integrate to get back asinh
    dp = rs_diff(p, x)
    p_squared = rs_square(p, x, prec)
    denom = p_squared + R(1)
    p1 = rs_nth_root(denom, -2, x, prec - 1)
    p1 = rs_mul(dp, p1, x, prec - 1)
    return rs_integrate(p1, x) + const

