
def vec_get_item_unsafe_lower(
    builder: LowLevelIRBuilder, base: Value, index: Value, line: int, *, can_borrow: bool = False
) -> Value:
    """Generate the low-level IR for an unsafe vec item load."""
    assert isinstance(base.type, RVec)
    index = as_platform_int(builder, index, line)
    vtype = base.type
    item_addr = vec_item_ptr(builder, base, index)
    result = vec_load_mem_item(builder, item_addr, vtype.item_type, can_borrow=can_borrow)
    builder.add_keep_alive(base, KEEP_ALIVE_SHORT_LIVED)
    return result

