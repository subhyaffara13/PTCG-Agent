
def as_platform_int(builder: LowLevelIRBuilder, v: Value, line: int) -> Value:
    rtype = v.type
    if is_c_py_ssize_t_rprimitive(rtype):
        return v
    if isinstance(v, Integer):
        if is_short_int_rprimitive(rtype) or is_int_rprimitive(rtype):
            return Integer(v.value // 2, c_pyssize_t_rprimitive)
        return Integer(v.value, c_pyssize_t_rprimitive)
    if isinstance(rtype, RPrimitive):
        if PLATFORM_SIZE == 8 and is_int64_rprimitive(rtype):
            return v
        if PLATFORM_SIZE == 4 and is_int32_rprimitive(rtype):
            return v
    return builder.coerce(v, c_pyssize_t_rprimitive, line)

