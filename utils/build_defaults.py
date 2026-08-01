
def buildDefaults(table):
    d = {}
    for op, name, arg, default, conv in table:
        if default is not None:
            d[name] = default
    return d

