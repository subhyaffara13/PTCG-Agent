
def stringToLong(s):
    if len(s) != 4:
        raise ValueError("string must be 4 bytes long")
    l = 0
    for i in range(4):
        l += byteord(s[i]) << (i * 8)
    return l

