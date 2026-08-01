
def translate_all_call(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if (
        len(expr.args) == 1
        and expr.arg_kinds == [ARG_POS]
        and isinstance(expr.args[0], GeneratorExpr)
    ):
        return any_all_helper(
            builder,
            expr.args[0],
            builder.true,
            lambda x: builder.unary_op(x, "not", expr.line),
            builder.false,
        )
    return None

