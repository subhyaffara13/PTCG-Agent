
def iter_iterindices(i):
    ret = []
    while not i.finished:
        ret.append(i.iterindex)
        i.iternext()
    return ret

