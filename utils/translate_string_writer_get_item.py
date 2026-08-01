
def translate_string_writer_get_item(
    builder: IRBuilder, base_expr: Expression, args: list[Expression], ctx_expr: Expression
) -> Value | None:
    """Optimized StringWriter.__getitem__ implementation with bounds checking."""
    return translate_getitem_with_bounds_check(
        builder,
        base_expr,
        args,
        ctx_expr,
        string_writer_adjust_index_op,
        string_writer_range_check_op,
        string_writer_get_item_unsafe_op,
    )

