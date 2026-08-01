
def _flags_fromnum(num):
    res = []
    for key in _flagnames:
        value = mu._flagdict[key]
        if (num & value):
            res.append(key)
    return res

