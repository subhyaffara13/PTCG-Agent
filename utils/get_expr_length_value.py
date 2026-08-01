
def get_expr_length_value(
    builder: IRBuilder, expr: Expression, expr_reg: Value, line: int, use_pyssize_t: bool
) -> Value:
    rtype = builder.node_type(expr)
    assert is_sequence_rprimitive(rtype) or isinstance(rtype, (RTuple, RVec)), rtype
    length = get_expr_length(builder, expr)
    if length is None:
        # We cannot compute the length at compile time, so we will fetch it.
        return builder.builder.builtin_len(expr_reg, line, use_pyssize_t=use_pyssize_t)
    # The expression result is known at compile time, so we can use a constant.
    return Integer(length, c_pyssize_t_rprimitive if use_pyssize_t else short_int_rprimitive)

