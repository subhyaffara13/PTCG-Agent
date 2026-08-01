
def readCard32(file):
    (value,) = struct.unpack(">L", file.read(4))
    return value

