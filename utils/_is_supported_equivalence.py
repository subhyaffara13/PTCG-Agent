
def _is_supported_equivalence(
    expr: sympy.Expr,
) -> TypeGuard[sympy.Add | sympy.Mul | sympy.Symbol]:
    # Currently supported Dim ops are linear expressions with integer coefficients.
    # So check that expr only contains +, *, ints, and a single occurrence of a symbol.
    # (See also documentation of dynamic_shapes._DerivedDim.)
    if isinstance(expr, (sympy.Add, sympy.Mul)):
        if len(expr.args) > 2:
            return False
        lhs, rhs = expr.args
        return (_is_supported_equivalence(lhs) and isinstance(rhs, sympy.Integer)) or (
            isinstance(lhs, sympy.Integer) and _is_supported_equivalence(rhs)
        )
    return isinstance(expr, sympy.Symbol)

