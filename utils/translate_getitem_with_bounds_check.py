
def translate_getitem_with_bounds_check(
    builder: IRBuilder,
    base_expr: Expression,
    args: list[Expression],
    ctx_expr: Expression,
    adjust_index_op: PrimitiveDescription,
    range_check_op: PrimitiveDescription,
    get_item_unsafe_op: PrimitiveDescription,
) -> Value | None:
    """Shared helper for optimized __getitem__ with bounds checking.

    This implements the common pattern of:
    1. Adjusting negative indices
    2. Checking if index is in valid range
    3. Raising IndexError if out of range
    4. Getting the item if in range

    Args:
        builder: The IR builder
        base_expr: The base object expression
        args: The arguments to __getitem__ (should be length 1)
        ctx_expr: The context expression for line numbers
        adjust_index_op: Primitive op to adjust negative indices
        range_check_op: Primitive op to check if index is in valid range
        get_item_unsafe_op: Primitive op to get item (no bounds checking)

    Returns:
        The result value, or None if optimization doesn't apply
    """
    # Check that we have exactly one argument
    if len(args) != 1:
        return None

    # Get the object
    obj = builder.accept(base_expr)

    # Get the index argument
    index = builder.accept(args[0])

    # Adjust the index (handle negative indices)
    adjusted_index = builder.primitive_op(adjust_index_op, [obj, index], ctx_expr.line)

    # Check if the adjusted index is in valid range
    range_check = builder.primitive_op(range_check_op, [obj, adjusted_index], ctx_expr.line)

    # Create blocks for branching
    valid_block = BasicBlock()
    invalid_block = BasicBlock()

    builder.add_bool_branch(range_check, valid_block, invalid_block)

    # Handle invalid index - raise IndexError
    builder.activate_block(invalid_block)
    builder.add(
        RaiseStandardError(RaiseStandardError.INDEX_ERROR, "index out of range", ctx_expr.line)
    )
    builder.add(Unreachable())

    # Handle valid index - get the item
    builder.activate_block(valid_block)
    result = builder.primitive_op(get_item_unsafe_op, [obj, adjusted_index], ctx_expr.line)

    return result

