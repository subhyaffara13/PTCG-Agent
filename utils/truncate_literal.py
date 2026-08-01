
def truncate_literal(value: Value, rtype: RPrimitive) -> Value:
    """If value is an integer literal value, truncate it to given native int rtype.

    For example, truncate 256 into 0 if rtype is u8.
    """
    if not isinstance(value, Integer):
        return value  # Not a literal, nothing to do
    x = value.numeric_value()
    max_unsigned = (1 << (rtype.size * 8)) - 1
    x = x & max_unsigned
    if rtype.is_signed and x >= (max_unsigned + 1) // 2:
        # Adjust to make it a negative value
        x -= max_unsigned + 1
    return Integer(x, rtype)

