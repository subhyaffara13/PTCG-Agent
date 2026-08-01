
def is_fixed_width_rtype(rtype: RType) -> TypeGuard[RPrimitive]:
    return (
        is_int64_rprimitive(rtype)
        or is_int32_rprimitive(rtype)
        or is_int16_rprimitive(rtype)
        or is_uint8_rprimitive(rtype)
    )

