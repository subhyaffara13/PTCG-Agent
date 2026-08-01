
def translate_int(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) != 1 or expr.arg_kinds[0] != ARG_POS:
        return None
    arg = expr.args[0]
    arg_type = builder.node_type(arg)
    if (
        is_bool_rprimitive(arg_type)
        or is_int_rprimitive(arg_type)
        or is_fixed_width_rtype(arg_type)
    ):
        src = builder.accept(arg)
        return builder.coerce(src, int_rprimitive, expr.line)
    return None

