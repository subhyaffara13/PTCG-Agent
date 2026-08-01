
def transform_yield_from_expr(builder: IRBuilder, o: YieldFromExpr) -> Value:
    return emit_yield_from_or_await(builder, builder.accept(o.expr), o.line, is_await=False)

