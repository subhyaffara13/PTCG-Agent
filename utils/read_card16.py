
def readCard16(file):
    (value,) = struct.unpack(">H", file.read(2))
    return value

