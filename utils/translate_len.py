
def translate_len(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) == 1 and expr.arg_kinds == [ARG_POS]:
        arg = expr.args[0]
        expr_rtype = builder.node_type(arg)
        # NOTE (?) I'm not sure if my handling of can_borrow is correct here
        obj = builder.accept(
            arg, can_borrow=is_list_rprimitive(expr_rtype) or isinstance(expr_rtype, RVec)
        )
        if is_sequence_rprimitive(expr_rtype) or isinstance(expr_rtype, RTuple):
            return get_expr_length_value(builder, arg, obj, expr.line, use_pyssize_t=False)
        else:
            # TODO: Decide type of result based on context somehow?
            if isinstance(obj.type, RVec):
                return builder.builtin_len(obj, expr.line, use_pyssize_t=True)
            else:
                return builder.builtin_len(obj, expr.line)
    return None

