
def encodeFixed(f, pack=struct.pack):
    """For T2 only"""
    value = floatToFixed(f, precisionBits=16)
    if value & 0xFFFF == 0:  # check if the fractional part is zero
        return encodeIntT2(value >> 16)  # encode only the integer part
    else:
        return b"\xff" + pack(">l", value)  # encode the entire fixed point value

