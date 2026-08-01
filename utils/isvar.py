
def isvar(v):
    return True


def isvar(o):
    return _glv and hashable(o) and o in _glv

