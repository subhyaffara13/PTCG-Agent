
def longToString(long):
    s = b""
    for i in range(4):
        s += bytechr((long & (0xFF << (i * 8))) >> i * 8)
    return s

