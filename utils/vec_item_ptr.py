
def vec_item_ptr(builder: LowLevelIRBuilder, vecobj: Value, index: Value) -> Value:
    items_addr = vec_items(builder, vecobj)
    assert isinstance(vecobj.type, RVec)
    # TODO: Do we need to care about alignment?
    item_type = vecobj.type.item_type
    if isinstance(item_type, RPrimitive):
        item_size = item_type.size
    elif isinstance(item_type, RVec):
        item_size = 2 * PLATFORM_SIZE
    else:
        item_size = object_rprimitive.size
    delta = builder.int_mul(index, item_size)
    return builder.int_add(items_addr, delta)

