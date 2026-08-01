
def _chk2_asarray(a, b, axis):
    a = ma.asanyarray(a)
    b = ma.asanyarray(b)
    if axis is None:
        a = ma.ravel(a)
        b = ma.ravel(b)
        outaxis = 0
    else:
        outaxis = axis
    return a, b, outaxis

