
def allexcept(*args):
    newcats = cats[:]
    for arg in args:
        newcats.remove(arg)
    return ''.join(globals()[cat] for cat in newcats)


def allexcept(*args):
    newcats = cats[:]
    for arg in args:
        newcats.remove(arg)
    return ''.join(globals()[cat] for cat in newcats)

