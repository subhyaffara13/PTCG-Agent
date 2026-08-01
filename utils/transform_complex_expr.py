
def transform_complex_expr(builder: IRBuilder, expr: ComplexExpr) -> Value:
    return builder.builder.load_complex(expr.value)

