
def is_int32_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return rtype is int32_rprimitive or (
        rtype is c_pyssize_t_rprimitive and rtype._ctype == "int32_t"
    )

