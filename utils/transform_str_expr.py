
def transform_str_expr(builder: IRBuilder, expr: StrExpr) -> Value:
    return builder.load_str(expr.value)

