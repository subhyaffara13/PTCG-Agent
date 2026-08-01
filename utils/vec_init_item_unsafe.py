
def vec_init_item_unsafe(
    builder: LowLevelIRBuilder, base: Value, index: Value, item: Value, line: int
) -> None:
    assert isinstance(base.type, RVec)
    index = as_platform_int(builder, index, line)
    vtype = base.type
    item_addr = vec_item_ptr(builder, base, index)
    item_type = vtype.item_type
    item = builder.coerce(item, item_type, line)
    vec_set_mem_item(builder, item_addr, item_type, item)
    builder.keep_alive([base], line)

