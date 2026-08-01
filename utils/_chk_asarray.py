
def _chk_asarray(a, axis):
    # Always returns a masked array, raveled for axis=None
    a = ma.asanyarray(a)
    if axis is None:
        a = ma.ravel(a)
        outaxis = 0
    else:
        outaxis = axis
    return a, outaxis


def _chk_asarray(a, axis, *, xp=None):
    if xp is None:
        xp = array_namespace(a)

    if axis is None:
        a = xp.reshape(a, (-1,))
        outaxis = 0
    else:
        a = xp.asarray(a)
        outaxis = axis

    if a.ndim == 0:
        a = xp.reshape(a, (-1,))

    return a, outaxis

