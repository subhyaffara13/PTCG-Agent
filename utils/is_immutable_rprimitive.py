
def is_immutable_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return (
        is_str_rprimitive(rtype)
        or is_bytes_rprimitive(rtype)
        or is_tuple_rprimitive(rtype)
        or is_frozenset_rprimitive(rtype)
    )

