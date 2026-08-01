
def translate_vec_append(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) == 2 and expr.arg_kinds == [ARG_POS, ARG_POS]:
        vec_arg = expr.args[0]
        item_arg = expr.args[1]
        vec_type = builder.node_type(vec_arg)
        if isinstance(vec_type, RVec):
            vec_value = builder.accept(vec_arg)
            arg_value = builder.accept(item_arg)
            return vec_append(builder.builder, vec_value, arg_value, item_arg.line)
    return None

