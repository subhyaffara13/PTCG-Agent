
def npp_polyvalfromroots(x, r, *, xp, tensor=True):
    r = xpx.atleast_nd(r, ndim=1, xp=xp)
    # if r.dtype.char in '?bBhHiIlLqQpP':
    #    r = r.astype(np.double)

    if isinstance(x, tuple | list):
        x = xp.asarray(x)

    if tensor:
        r = xp.reshape(r, r.shape + (1,) * x.ndim)
    elif x.ndim >= r.ndim:
        raise ValueError("x.ndim must be < r.ndim when tensor == False")
    return xp.prod(x - r, axis=0)

