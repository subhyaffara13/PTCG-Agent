
def decompose_power_rat(expr: Expr) -> tuple[Expr, Rational]:
    """
    Decompose power into symbolic base and rational exponent;
    if the exponent is not a Rational, then separate only the
    integer coefficient.

    Examples
    ========

    >>> from sympy.core.exprtools import decompose_power_rat
    >>> from sympy.abc import x
    >>> from sympy import sqrt, exp

    >>> decompose_power_rat(sqrt(x))
    (x, 1/2)
    >>> decompose_power_rat(exp(-3*x/2))
    (exp(x/2), -3)

    """
    base, exp = expr.as_base_exp()
    if not exp.is_Rational:
        base, exp_i = decompose_power(expr)
        exp = Integer(exp_i)
    return base, exp # type: ignore

