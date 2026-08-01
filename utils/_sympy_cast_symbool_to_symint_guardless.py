
def _sympy_cast_symbool_to_symint_guardless(x: SympyBoolean) -> sympy.Expr:
    return sympy.Piecewise((1, x), (0, True))

