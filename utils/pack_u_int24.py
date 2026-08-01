
def packUInt24(value):
    assert 0 <= value < 0x1000000, value
    return struct.pack(">I", value)[1:]

