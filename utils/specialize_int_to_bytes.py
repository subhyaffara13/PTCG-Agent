
def specialize_int_to_bytes(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    # int.to_bytes(length, byteorder, signed=False)
    if any(kind not in (ARG_POS, ARG_NAMED) for kind in expr.arg_kinds):
        return None
    if not isinstance(callee, MemberExpr):
        return None
    length_expr: Expression | None = None
    byteorder_expr: Expression | None = None
    signed_expr: Expression | None = None
    positional_index = 0
    for name, arg in zip(expr.arg_names, expr.args):
        if name is None:
            if positional_index == 0:
                length_expr = arg
            elif positional_index == 1:
                byteorder_expr = arg
            elif positional_index == 2:
                signed_expr = arg
            else:
                return None
            positional_index += 1
        elif name == "length":
            if length_expr is not None:
                return None
            length_expr = arg
        elif name == "byteorder":
            if byteorder_expr is not None:
                return None
            byteorder_expr = arg
        elif name == "signed":
            if signed_expr is not None:
                return None
            signed_expr = arg
        else:
            return None
    if length_expr is None or byteorder_expr is None:
        return None

    signed_is_bool = True
    if signed_expr is not None:
        signed_is_bool = is_bool_rprimitive(builder.node_type(signed_expr))
    if not (
        is_int_rprimitive(builder.node_type(length_expr))
        and is_str_rprimitive(builder.node_type(byteorder_expr))
        and signed_is_bool
    ):
        return None

    self_arg = builder.accept(callee.expr)
    length_arg = builder.accept(length_expr)
    if signed_expr is None:
        signed_arg = builder.false()
    else:
        signed_arg = builder.accept(signed_expr)
    if isinstance(byteorder_expr, StrExpr):
        if byteorder_expr.value == "little":
            return builder.call_c(
                int_to_little_endian_op, [self_arg, length_arg, signed_arg], expr.line
            )
        elif byteorder_expr.value == "big":
            return builder.call_c(
                int_to_big_endian_op, [self_arg, length_arg, signed_arg], expr.line
            )
    # Fallback to generic primitive op
    byteorder_arg = builder.accept(byteorder_expr)
    return builder.call_c(
        int_to_bytes_op, [self_arg, length_arg, byteorder_arg, signed_arg], expr.line
    )

