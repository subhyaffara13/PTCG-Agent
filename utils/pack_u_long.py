
def packULong(value):
    assert 0 <= value < 0x100000000, value
    return struct.pack(">I", value)

