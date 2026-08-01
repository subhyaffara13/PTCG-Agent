
def list_items(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    ob_item_ptr = builder.add(GetElementPtr(args[0], PyListObject, "ob_item", line))
    return builder.load_mem(ob_item_ptr, pointer_rprimitive)

