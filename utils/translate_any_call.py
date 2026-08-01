
def translate_any_call(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if (
        len(expr.args) == 1
        and expr.arg_kinds == [ARG_POS]
        and isinstance(expr.args[0], GeneratorExpr)
    ):
        return any_all_helper(builder, expr.args[0], builder.false, lambda x: x, builder.true)
    return None

