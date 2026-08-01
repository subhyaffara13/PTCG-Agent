
def unsafe_index(builder: IRBuilder, target: Value, index: Value, line: int) -> Value:
    """Emit a potentially unsafe index into a target."""
    # This doesn't really fit nicely into any of our data-driven frameworks
    # since we want to use __getitem__ if we don't have an unsafe version,
    # so we just check manually.
    if is_list_rprimitive(target.type):
        if not IS_FREE_THREADED:
            return builder.primitive_op(list_get_item_unsafe_op, [target, index], line)
        else:
            return builder.primitive_op(list_get_item_int64_op, [target, index], line)
    elif is_tuple_rprimitive(target.type):
        return builder.call_c(tuple_get_item_unsafe_op, [target, index], line)
    elif is_str_rprimitive(target.type):
        return builder.call_c(str_get_item_unsafe_op, [target, index], line)
    elif isinstance(target.type, RVec):
        return vec_get_item_unsafe(builder.builder, target, index, line)
    else:
        return builder.gen_method_call(target, "__getitem__", [index], None, line)

