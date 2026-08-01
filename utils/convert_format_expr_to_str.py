
def convert_format_expr_to_str(
    builder: IRBuilder, format_ops: list[FormatOp], exprs: list[Expression], line: int
) -> list[Value] | None:
    """Convert expressions into string literal objects with the guidance
    of FormatOps. Return None when fails."""
    if len(format_ops) != len(exprs):
        return None

    converted = []
    for x, format_op in zip(exprs, format_ops):
        node_type = builder.node_type(x)
        if format_op == FormatOp.STR:
            if isinstance(folded := constant_fold_expr(builder, x), str):
                var_str = builder.load_literal_value(folded)
            elif is_str_rprimitive(node_type):
                var_str = builder.accept(x)
            elif is_int_rprimitive(node_type) or is_short_int_rprimitive(node_type):
                var_str = builder.primitive_op(int_to_str_op, [builder.accept(x)], line)
            else:
                var_str = builder.primitive_op(str_op, [builder.accept(x)], line)
        elif format_op == FormatOp.INT:
            if isinstance(folded := constant_fold_expr(builder, x), int):
                var_str = builder.load_literal_value(str(folded))
            elif is_int_rprimitive(node_type) or is_short_int_rprimitive(node_type):
                var_str = builder.primitive_op(int_to_str_op, [builder.accept(x)], line)
            else:
                return None
        else:
            return None
        converted.append(var_str)
    return converted

