
def is_sequence_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return isinstance(rtype, RPrimitive) and (
        is_list_rprimitive(rtype)
        or is_tuple_rprimitive(rtype)
        or is_str_rprimitive(rtype)
        or is_bytes_rprimitive(rtype)
        or is_bytearray_rprimitive(rtype)
    )

