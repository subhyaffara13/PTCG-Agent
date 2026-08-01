
def transform_await_expr(builder: IRBuilder, o: AwaitExpr) -> Value:
    return emit_yield_from_or_await(builder, builder.accept(o.expr), o.line, is_await=True)

