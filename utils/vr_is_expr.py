
def vr_is_expr(vr: ValueRanges[_T]) -> TypeGuard[ValueRanges[sympy.Expr]]:
    return not vr.is_bool

