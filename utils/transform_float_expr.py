
def transform_float_expr(builder: IRBuilder, expr: FloatExpr) -> Value:
    return builder.builder.load_float(expr.value)

