
def translate_cast_expr(builder: IRBuilder, expr: CastExpr) -> Value:
    src = builder.accept(expr.expr)
    target_type = builder.type_to_rtype(expr.type)
    return builder.coerce(src, target_type, expr.line)

