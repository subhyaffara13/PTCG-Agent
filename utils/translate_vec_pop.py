
def translate_vec_pop(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if 1 <= len(expr.args) <= 2 and all(kind == ARG_POS for kind in expr.arg_kinds):
        vec_arg = expr.args[0]
        vec_type = builder.node_type(vec_arg)
        if isinstance(vec_type, RVec):
            vec_value = builder.accept(vec_arg)
            if len(expr.args) == 2:
                index_value = builder.accept(expr.args[1])
            else:
                index_value = Integer(-1, int64_rprimitive)
            return vec_pop(builder.builder, vec_value, index_value, vec_arg.line)
    return None

