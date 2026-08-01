
def _poly1d(c_or_r, *, xp):
    """ Constructor of np.poly1d object from an array of coefficients (r=False)
    """
    c_or_r = xpx.atleast_nd(c_or_r, ndim=1, xp=xp)
    if c_or_r.ndim > 1:
        raise ValueError("Polynomial must be 1d only.")
    c_or_r = _trim_zeros(c_or_r, trim='f')
    if c_or_r.shape[0] == 0:
        c_or_r = xp.asarray([0], dtype=c_or_r.dtype)
    return c_or_r

