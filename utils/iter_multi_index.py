
def iter_multi_index(i):
    ret = []
    while not i.finished:
        ret.append(i.multi_index)
        i.iternext()
    return ret

