
def upper_bound(val: _ExprType):
    return bound_sympy(val).upper if isinstance(val, sympy.Expr) else val

