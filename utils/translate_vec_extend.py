
def translate_vec_extend(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) == 2 and expr.arg_kinds == [ARG_POS, ARG_POS]:
        vec_arg = expr.args[0]
        iter_arg = expr.args[1]
        vec_type = builder.node_type(vec_arg)
        if isinstance(vec_type, RVec):
            vec_value = builder.accept(vec_arg)
            iter_value = builder.accept(iter_arg)
            return vec_extend(builder.builder, vec_value, iter_value, iter_arg.line)
    return None

