
def try_optimize_int_floor_divide(builder: IRBuilder, expr: OpExpr) -> OpExpr:
    """Replace // with a power of two with a right shift, if possible."""
    divisor = constant_fold_expr(builder, expr.right)
    if not isinstance(divisor, int):
        return expr
    shift = divisor.bit_length() - 1
    if 0 < shift < 28 and divisor == (1 << shift):
        new_expr = OpExpr(">>", expr.left, IntExpr(shift))
        new_expr.line = expr.line
        return new_expr
    return expr

