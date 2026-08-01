
def read_longInt(self, b0, data, index):
    (value,) = struct.unpack(">l", data[index : index + 4])
    return value, index + 4

