
def calcSubrBias(subrs):
    nSubrs = len(subrs)
    if nSubrs < 1240:
        bias = 107
    elif nSubrs < 33900:
        bias = 1131
    else:
        bias = 32768
    return bias

