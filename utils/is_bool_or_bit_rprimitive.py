
def is_bool_or_bit_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return is_bool_rprimitive(rtype) or is_bit_rprimitive(rtype)

