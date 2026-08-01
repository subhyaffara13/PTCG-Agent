
def translate_float(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) != 1 or expr.arg_kinds[0] != ARG_POS:
        return None
    arg = expr.args[0]
    arg_type = builder.node_type(arg)
    if is_float_rprimitive(arg_type):
        # No-op float conversion.
        return builder.accept(arg)
    return None

