
def vec_len(builder: LowLevelIRBuilder, val: Value) -> Value:
    """Return len(<vec>) as i64."""
    len_val = vec_len_native(builder, val)
    if IS_32_BIT_PLATFORM:
        return builder.coerce(len_val, int64_rprimitive, -1)
    return len_val

