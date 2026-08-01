
def read_fixed1616(self, b0, data, index):
    (value,) = struct.unpack(">l", data[index : index + 4])
    return fixedToFloat(value, precisionBits=16), index + 4

