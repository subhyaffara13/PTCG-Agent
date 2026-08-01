
def vec_create_from_values(
    builder: LowLevelIRBuilder,
    vtype: RVec,
    values: list[Value],
    line: int,
    *,
    capacity: Value | None = None,
) -> Value:
    vec = vec_create(builder, vtype, len(values), line, capacity=capacity)
    ptr = vec_items(builder, vec)
    item_type = vtype.item_type
    step = step_size(item_type)
    for value in values:
        vec_set_mem_item(builder, ptr, item_type, value)
        ptr = builder.int_add(ptr, step)
    builder.keep_alive([vec], line)
    return vec

