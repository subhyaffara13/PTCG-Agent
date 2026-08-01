
def vec_load_mem_item(
    builder: LowLevelIRBuilder, ptr: Value, item_type: RType, *, can_borrow: bool = False
) -> Value:
    """Load a vec item from storage, converting nested vec slots to RVec values."""
    return builder.load_mem(ptr, item_type, borrow=can_borrow)

