
def transform_unary_expr(builder: IRBuilder, expr: UnaryExpr) -> Value:
    folded = try_constant_fold(builder, expr)
    if folded:
        return folded

    return builder.unary_op(builder.accept(expr.expr), expr.op, expr.line)

