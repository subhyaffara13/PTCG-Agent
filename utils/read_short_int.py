
def read_shortInt(self, b0, data, index):
    (value,) = struct.unpack(">h", data[index : index + 2])
    return value, index + 2

