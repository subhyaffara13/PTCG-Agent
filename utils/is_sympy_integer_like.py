
def is_sympy_integer_like(expr: object):
    """ "
    Is this expression a Sympy Integer or is it an integer sympy Expr
    containing no free symbols. The latter case can happen with Identity expr.
    """
    if not isinstance(expr, sympy.Expr):
        return False
    return isinstance(expr, sympy.Integer) or (
        expr.is_integer and len(expr.free_symbols) == 0
    )

