
def _broadcast_concatenate(arrays, axis, paired=False, xp=None):
    """Concatenate arrays along an axis with broadcasting."""
    xp = array_namespace(*arrays) if xp is None else xp
    arrays = _broadcast_arrays(arrays, axis if not paired else None, xp=xp)
    res = xp.concat(arrays, axis=axis)
    return res

