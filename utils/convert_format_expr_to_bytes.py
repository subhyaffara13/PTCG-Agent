
def convert_format_expr_to_bytes(
    builder: IRBuilder, format_ops: list[FormatOp], exprs: list[Expression], line: int
) -> list[Value] | None:
    """Convert expressions into bytes literal objects with the guidance
    of FormatOps. Return None when fails."""
    if len(format_ops) != len(exprs):
        return None

    converted = []
    for x, format_op in zip(exprs, format_ops):
        node_type = builder.node_type(x)
        # conversion type 's' is an alias of 'b' in bytes formatting
        if format_op == FormatOp.BYTES or format_op == FormatOp.STR:
            if is_bytes_rprimitive(node_type):
                var_bytes = builder.accept(x)
            else:
                return None
        elif format_op == FormatOp.INT:
            if isinstance(folded := constant_fold_expr(builder, x), int):
                var_bytes = builder.load_literal_value(str(folded).encode("ascii"))
            elif is_int_rprimitive(node_type) or is_short_int_rprimitive(node_type):
                var_bytes = builder.call_c(int_to_ascii_op, [builder.accept(x)], line)
            else:
                return None
        converted.append(var_bytes)
    return converted

