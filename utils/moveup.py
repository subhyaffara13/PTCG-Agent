
def moveup(l, x):
    return [e.xreplace({x: exp(x)}) for e in l]

