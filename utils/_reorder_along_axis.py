
def _reorder_along_axis(x, i, *, axis, xp):
    if is_jax(xp):
        return xp.put_along_axis(x, i, values=x, axis=axis, inplace=False)
    if hasattr(xp, 'put_along_axis'):
        xp.put_along_axis(x, i, values=x.copy(), axis=axis)
        return x
    else:
        return xp.take_along_axis(x, xp.argsort(i, axis=-1), axis=-1)

