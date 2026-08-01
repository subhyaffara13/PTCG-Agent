
def vec_get_item_unsafe(
    builder: LowLevelIRBuilder, base: Value, index: Value, line: int, *, can_borrow: bool = False
) -> Value:
    """Get vec item, assuming index is non-negative and within bounds.

    This emits a generic primitive op that is inlined during lowering.
    """
    assert isinstance(base.type, RVec)
    if can_borrow:
        desc = vec_get_item_unsafe_borrow_op
    else:
        desc = vec_get_item_unsafe_op
    return builder.primitive_op(desc, [base, index], line, type_args=[base.type.item_type])


def vec_get_item_unsafe(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    base, index = args
    return vec_get_item_unsafe_lower(builder, base, index, line, can_borrow=False)

