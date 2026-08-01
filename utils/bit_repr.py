
def bitRepr(value: int, bits: int) -> str:
    s = ""
    for i in range(bits):
        s = "01"[value & 0x1] + s
        value = value >> 1
    return s

