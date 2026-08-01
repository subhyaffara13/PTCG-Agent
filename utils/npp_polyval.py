
def npp_polyval(x, c, *, xp, tensor=True):
    if xp.isdtype(c.dtype, 'integral'):
        c = xp.astype(c, xp_default_dtype(xp))

    c = xpx.atleast_nd(c, ndim=1, xp=xp)
    if isinstance(x, tuple | list):
        x = xp.asarray(x)
    if tensor:
        c = xp.reshape(c, (c.shape + (1,)*x.ndim))

    c0, _ = xp_promote(c[-1, ...], x, broadcast=True, xp=xp)
    for i in range(2, c.shape[0] + 1):
        c0 = c[-i, ...] + c0*x
    return c0

