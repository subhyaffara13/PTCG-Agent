
def packPStrings(strings):
    data = b""
    for s in strings:
        data = data + bytechr(len(s)) + tobytes(s, encoding="latin1")
    return data

