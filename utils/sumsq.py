
def sumsq(a, b, xp=None):
    xp = array_namespace(a, b) if xp is None else xp
    return xp.sqrt(xp.sum((a - b)**2))

