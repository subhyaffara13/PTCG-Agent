
def big_endian_uint32(i):
    """Return the 32 bit unsigned integer big-endian representation of i"""

    s = struct.pack(">I", i)
    return struct.unpack("=I", s)[0]

