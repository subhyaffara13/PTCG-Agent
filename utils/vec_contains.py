
def vec_contains(builder: LowLevelIRBuilder, vec: Value, target: Value, line: int) -> Value:
    assert isinstance(vec.type, RVec)
    vec_type = vec.type
    item_type = vec_type.item_type
    target = builder.coerce(target, item_type, line)

    step = step_size(item_type)
    len_val = vec_len_native(builder, vec)
    items_start = vec_items(builder, vec)
    items_end = builder.int_add(items_start, builder.int_mul(len_val, step))

    true, end = BasicBlock(), BasicBlock()

    for_loop = builder.begin_for(
        items_start, items_end, Integer(step, c_pyssize_t_rprimitive), signed=False
    )
    item = vec_load_mem_item(builder, for_loop.index, item_type, can_borrow=True)
    comp = builder.binary_op(item, target, "==", line)
    false = BasicBlock()
    builder.add(Branch(comp, true, false, Branch.BOOL))
    builder.activate_block(false)
    for_loop.finish()

    builder.keep_alive([vec], line)

    res = Register(bool_rprimitive)
    builder.assign(res, Integer(0, bool_rprimitive))
    builder.goto(end)
    builder.activate_block(true)
    builder.assign(res, Integer(1, bool_rprimitive))
    builder.goto_and_activate(end)
    return res

