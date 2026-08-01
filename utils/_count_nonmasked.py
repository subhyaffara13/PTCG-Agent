
def _count_nonmasked(x, axis, keepdims=False, xp=None):
    xp = array_namespace(x) if xp is None else xp
    if is_marray(xp):
        if np.iterable(axis):
            message = '`axis` must be an integer or None for use with `MArray`.'
            raise NotImplementedError(message)
        return xp.astype(xp.count(x, axis=axis, keepdims=keepdims), x.dtype)
    return (xp_size(x) if axis is None else
            # compact way to deal with axis tuples or ints
            int(np.prod(np.asarray(x.shape)[np.asarray(axis)])))

