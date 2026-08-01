
def _getmaxmin(t):
    from numpy._core import getlimits
    f = getlimits.finfo(t)
    return f.max, f.min

