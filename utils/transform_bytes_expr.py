
def transform_bytes_expr(builder: IRBuilder, expr: BytesExpr) -> Value:
    return builder.load_bytes_from_str_literal(expr.value)

