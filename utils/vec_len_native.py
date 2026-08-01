
def vec_len_native(builder: LowLevelIRBuilder, val: Value) -> Value:
    """Return len(<vec>) as platform integer type (32-bit/64-bit)."""
    return builder.get_element(val, "len")

