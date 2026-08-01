
def buildOpcodeDict(table):
    d = {}
    for op, name, arg, default, conv in table:
        if isinstance(op, tuple):
            op = bytechr(op[0]) + bytechr(op[1])
        else:
            op = bytechr(op)
        d[name] = (op, arg)
    return d

