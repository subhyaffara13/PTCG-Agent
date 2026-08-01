
def cvtFromUVS(val):
    assert 0 <= val < 0x1000000
    fourByteString = struct.pack(">L", val)
    return fourByteString[1:]

