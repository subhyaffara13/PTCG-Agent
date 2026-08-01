
def check_native_int_range(rtype: RPrimitive, n: int) -> bool:
    """Is n within the range of a native, fixed-width int type?

    Assume the type is a fixed-width int type.
    """
    if not rtype.is_signed:
        return 0 <= n < (1 << (8 * rtype.size))
    else:
        limit = 1 << (rtype.size * 8 - 1)
        return -limit <= n < limit

