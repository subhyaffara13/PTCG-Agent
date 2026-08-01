
def _unify(u, v, s):
    if len(u) != len(v):
        return False
    for uu, vv in zip(u, v):  # avoiding recursion
        s = unify(uu, vv, s)
        if s is False:
            return False
    return s


def _unify(u, v, s):
    """Unify a Python ``slice`` object"""
    return unify((u.start, u.stop, u.step), (v.start, v.stop, v.step), s)

