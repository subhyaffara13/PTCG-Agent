
def refine_re(expr, assumptions):
    """
    Handler for real part.

    Examples
    ========

    >>> from sympy.assumptions.refine import refine_re
    >>> from sympy import Q, re
    >>> from sympy.abc import x
    >>> refine_re(re(x), Q.real(x))
    x
    >>> refine_re(re(x), Q.imaginary(x))
    0
    """
    arg = expr.args[0]
    if ask(Q.real(arg), assumptions):
        return arg
    if ask(Q.imaginary(arg), assumptions):
        return S.Zero
    return _refine_reim(expr, assumptions)

