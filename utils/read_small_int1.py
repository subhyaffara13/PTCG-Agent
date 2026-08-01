
def read_smallInt1(self, b0, data, index):
    b1 = byteord(data[index])
    return (b0 - 247) * 256 + b1 + 108, index + 1

