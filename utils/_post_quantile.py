
def _post_quantile(res, p_mask, axis, axis_none, ndim, keepdims, xp):
    res = xpx.at(res, p_mask).set(xp.nan)

    # Reshape per axis/keepdims
    if axis_none and keepdims:
        shape = (1,)*(ndim - 1) + res.shape
        res = xp.reshape(res, shape)
        axis = -1

    res = xp.moveaxis(res, -1, axis)

    if not keepdims:
        res = xp.squeeze(res, axis=axis)

    return res[()] if res.ndim == 0 else res

