
def half_to_int(f: float) -> int:
    """Casts a half-precision float value into an integer.

    Converts a half precision floating point value, such as `torch.half` or
    `torch.bfloat16`, into an integer value which can be written into the
    half_val field of a TensorProto for storage.

    To undo the effects of this conversion, use int_to_half().

    """
    buf = struct.pack("f", f)
    return struct.unpack("i", buf)[0]

