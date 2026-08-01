
def list_item_ptr(builder: LowLevelIRBuilder, obj: Value, index: Value, line: int) -> Value:
    """Get a pointer to a list item (index must be valid and non-negative).

    Type of index must be c_pyssize_t_rprimitive, and obj must refer to a list object.
    """
    # List items are represented as an array of pointers. Pointer to the item obj[index] is
    # <pointer to first item> + index * <pointer size>.
    items = list_items(builder, [obj], line)
    delta = builder.add(
        IntOp(
            c_pyssize_t_rprimitive,
            index,
            Integer(PLATFORM_SIZE, c_pyssize_t_rprimitive),
            IntOp.MUL,
        )
    )
    return builder.add(IntOp(pointer_rprimitive, items, delta, IntOp.ADD))

