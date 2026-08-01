
def is_any_int(rtype: RType) -> bool:
    return is_tagged(rtype) or is_int32_rprimitive(rtype) or is_int64_rprimitive(rtype)

