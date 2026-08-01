
def translate_bytes_get_item(
    builder: IRBuilder, base_expr: Expression, args: list[Expression], ctx_expr: Expression
) -> Value | None:
    """Optimized bytes.__getitem__ implementation with bounds checking."""
    return translate_getitem_with_bounds_check(
        builder,
        base_expr,
        args,
        ctx_expr,
        bytes_adjust_index_op,
        bytes_range_check_op,
        bytes_get_item_unsafe_op,
    )

