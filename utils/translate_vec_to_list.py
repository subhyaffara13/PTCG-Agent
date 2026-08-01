
def translate_vec_to_list(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) == 1 and expr.arg_kinds == [ARG_POS]:
        arg_type = builder.node_type(expr.args[0])
        if isinstance(arg_type, RVec) and supports_vec_to_sequence(arg_type):
            vec = builder.accept(expr.args[0])
            return vec_to_list(builder.builder, vec, expr.line)
    return None

