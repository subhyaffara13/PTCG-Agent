
def transform_yield_expr(builder: IRBuilder, expr: YieldExpr) -> Value:
    if builder.fn_info.is_coroutine:
        builder.error("async generators are unimplemented", expr.line)

    if expr.expr:
        retval = builder.accept(expr.expr)
    else:
        retval = builder.builder.none()
    return emit_yield(builder, retval, expr.line)

