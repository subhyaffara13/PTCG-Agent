
def translate_i32(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) != 1 or expr.arg_kinds[0] != ARG_POS:
        return None
    arg = expr.args[0]
    arg_type = builder.node_type(arg)
    if is_int32_rprimitive(arg_type):
        return builder.accept(arg)
    elif is_int64_rprimitive(arg_type):
        val = builder.accept(arg)
        return builder.add(Truncate(val, int32_rprimitive, line=expr.line))
    elif is_int16_rprimitive(arg_type):
        val = builder.accept(arg)
        return builder.add(Extend(val, int32_rprimitive, signed=True, line=expr.line))
    elif is_uint8_rprimitive(arg_type):
        val = builder.accept(arg)
        return builder.add(Extend(val, int32_rprimitive, signed=False, line=expr.line))
    elif is_int_rprimitive(arg_type) or is_bool_rprimitive(arg_type):
        val = builder.accept(arg)
        val = truncate_literal(val, int32_rprimitive)
        return builder.coerce(val, int32_rprimitive, expr.line)
    return None

