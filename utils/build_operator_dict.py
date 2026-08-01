
def buildOperatorDict(table):
    d = {}
    for op, name, arg, default, conv in table:
        d[op] = (name, arg)
    return d


def buildOperatorDict(operatorList):
    oper = {}
    opc = {}
    for item in operatorList:
        if len(item) == 2:
            oper[item[0]] = item[1]
        else:
            oper[item[0]] = item[1:]
        if isinstance(item[0], tuple):
            opc[item[1]] = item[0]
        else:
            opc[item[1]] = (item[0],)
    return oper, opc

