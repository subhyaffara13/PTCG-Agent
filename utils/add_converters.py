
def addConverters(table):
    for i in range(len(table)):
        op, name, arg, default, conv = table[i]
        if conv is not None:
            continue
        if arg in ("delta", "array"):
            conv = ArrayConverter()
        elif arg == "number":
            conv = NumberConverter()
        elif arg == "SID":
            conv = ASCIIConverter()
        elif arg == "blendList":
            conv = None
        else:
            assert False
        table[i] = op, name, arg, default, conv

