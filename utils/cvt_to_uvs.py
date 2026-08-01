
def cvtToUVS(threeByteString):
    data = b"\0" + threeByteString
    (val,) = struct.unpack(">L", data)
    return val

