
def is_inexact(x, xp):
    # Determine whether `x` is of inexact (real of complex floating) dtype
    x = xp.asarray(x) if np.isscalar(x) or isinstance(x, list) else x
    dtype = getattr(x, 'dtype', x)
    return xp.isdtype(dtype, ('real floating', 'complex floating'))

