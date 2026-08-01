
def _angle(z, xp):
    """np.angle replacement
    """
    # XXX: https://github.com/data-apis/array-api/issues/595
    zimag = xp.imag(z) if xp.isdtype(z.dtype, 'complex floating') else 0.
    a = xp.atan2(zimag, xp.real(z))
    return a

