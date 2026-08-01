
def translate_bytes_writer_set_item(
    builder: IRBuilder, base_expr: Expression, args: list[Expression], ctx_expr: Expression
) -> Value | None:
    """Optimized BytesWriter.__setitem__ implementation with bounds checking."""
    # Check that we have exactly two arguments (index and value)
    if len(args) != 2:
        return None

    # Get the BytesWriter object
    obj = builder.accept(base_expr)

    # Get the index and value arguments
    index = builder.accept(args[0])
    value = builder.accept(args[1])

    # Adjust the index (handle negative indices)
    adjusted_index = builder.primitive_op(
        bytes_writer_adjust_index_op, [obj, index], ctx_expr.line
    )

    # Check if the adjusted index is in valid range
    range_check = builder.primitive_op(
        bytes_writer_range_check_op, [obj, adjusted_index], ctx_expr.line
    )

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

    # Handle valid index - set the item
    builder.activate_block(valid_block)
    builder.primitive_op(
        bytes_writer_set_item_unsafe_op, [obj, adjusted_index, value], ctx_expr.line
    )

    return builder.none()

