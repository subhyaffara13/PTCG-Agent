
def read_realNumber(self, b0, data, index):
    number = ""
    while True:
        b = byteord(data[index])
        index = index + 1
        nibble0 = (b & 0xF0) >> 4
        nibble1 = b & 0x0F
        if nibble0 == 0xF:
            break
        number = number + realNibbles[nibble0]
        if nibble1 == 0xF:
            break
        number = number + realNibbles[nibble1]
    return float(number), index

