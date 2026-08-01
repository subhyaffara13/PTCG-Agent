
def vec_set_mem_item(
    builder: LowLevelIRBuilder, ptr: Value, item_type: RType, item: Value
) -> None:
    """Store a vec item, converting RVec values to nested storage items."""
    builder.set_mem(ptr, item_type, item)

