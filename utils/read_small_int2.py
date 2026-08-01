
def read_smallInt2(self, b0, data, index):
    b1 = byteord(data[index])
    return -(b0 - 251) * 256 - b1 - 108, index + 1

