
def clear_coefficients(expr, rhs=S.Zero):
    """Return `p, r` where `p` is the expression obtained when Rational
    additive and multiplicative coefficients of `expr` have been stripped
    away in a naive fashion (i.e. without simplification). The operations
    needed to remove the coefficients will be applied to `rhs` and returned
    as `r`.

    Examples
    ========

    >>> from sympy.simplify.simplify import clear_coefficients
    >>> from sympy.abc import x, y
    >>> from sympy import Dummy
    >>> expr = 4*y*(6*x + 3)
    >>> clear_coefficients(expr - 2)
    (y*(2*x + 1), 1/6)

    When solving 2 or more expressions like `expr = a`,
    `expr = b`, etc..., it is advantageous to provide a Dummy symbol
    for `rhs` and  simply replace it with `a`, `b`, etc... in `r`.

    >>> rhs = Dummy('rhs')
    >>> clear_coefficients(expr, rhs)
    (y*(2*x + 1), _rhs/12)
    >>> _[1].subs(rhs, 2)
    1/6
    """
    was = None
    free = expr.free_symbols
    if expr.is_Rational:
        return (S.Zero, rhs - expr)
    while expr and was != expr:
        was = expr
        m, expr = (
            expr.as_content_primitive()
            if free else
            factor_terms(expr).as_coeff_Mul(rational=True))
        rhs /= m
        c, expr = expr.as_coeff_Add(rational=True)
        rhs -= c
    expr = signsimp(expr, evaluate = False)
    if expr.could_extract_minus_sign():
        expr = -expr
        rhs = -rhs
    return expr, rhs

