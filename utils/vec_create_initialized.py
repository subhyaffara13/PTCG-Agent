
def vec_create_initialized(
    builder: LowLevelIRBuilder,
    vtype: RVec,
    length: int | Value,
    init: Value,
    line: int,
    *,
    capacity: Value | None = None,
) -> Value:
    """Create vec with items initialized to the given value."""
    if isinstance(length, int):
        length = Integer(length, c_pyssize_t_rprimitive)
    length = as_platform_int(builder, length, line)

    item_type = vtype.item_type
    init = builder.coerce(init, item_type, line)
    vec = vec_create(builder, vtype, length, line, capacity=capacity)

    items_start = vec_items(builder, vec)
    step = step_size(item_type)
    items_end = builder.int_add(items_start, builder.int_mul(length, step))

    for_loop = builder.begin_for(
        items_start, items_end, Integer(step, c_pyssize_t_rprimitive), signed=False
    )
    vec_set_mem_item(builder, for_loop.index, item_type, init)
    for_loop.finish()

    builder.keep_alive([vec], line)
    return vec

