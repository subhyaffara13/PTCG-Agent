
def is_tagged(rtype: RType) -> TypeGuard[RPrimitive]:
    return rtype is int_rprimitive or rtype is short_int_rprimitive

