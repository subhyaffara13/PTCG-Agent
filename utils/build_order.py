
def buildOrder(table):
    l = []
    for op, name, arg, default, conv in table:
        l.append(name)
    return l

