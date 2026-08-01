
def transform_int_expr(builder: IRBuilder, expr: IntExpr) -> Value:
    return builder.builder.load_int(expr.value)

