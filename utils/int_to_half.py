
def int_to_half(i: int) -> float:
    """Casts an integer value to a half-precision float.

    Converts an integer value obtained from half_to_int back into a floating
    point value.

    """
    buf = struct.pack("i", i)
    return struct.unpack("f", buf)[0]

