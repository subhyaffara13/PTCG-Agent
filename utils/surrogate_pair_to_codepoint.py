
def surrogatePairToCodepoint(data):
    char_val = (0x10000 + (ord(data[0]) - 0xD800) * 0x400 +
                (ord(data[1]) - 0xDC00))
    return char_val

