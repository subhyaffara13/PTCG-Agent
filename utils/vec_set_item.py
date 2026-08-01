
def vec_set_item(
    builder: LowLevelIRBuilder, base: Value, index: Value, item: Value, line: int
) -> None:
    assert isinstance(base.type, RVec)
    vtype = base.type
    len_val = vec_len(builder, base)
    index = vec_check_and_adjust_index(builder, len_val, index, line)
    index = builder.coerce(index, c_pyssize_t_rprimitive, line)
    item_addr = vec_item_ptr(builder, base, index)
    item_type = vtype.item_type
    item = builder.coerce(item, item_type, line)
    if item_type.is_refcounted:
        # Read an unborrowed reference to cause a decref to be
        # generated for the old item.
        old_item = vec_load_mem_item(builder, item_addr, item_type, can_borrow=True)
        builder.add(DecRef(old_item))
    vec_set_mem_item(builder, item_addr, item_type, item)
    builder.keep_alive([base], line)

