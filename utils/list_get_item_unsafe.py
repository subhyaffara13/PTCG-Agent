
def list_get_item_unsafe(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    index = builder.coerce(args[1], c_pyssize_t_rprimitive, line)
    item_ptr = list_item_ptr(builder, args[0], index, line)
    return builder.load_mem(item_ptr, object_rprimitive)

