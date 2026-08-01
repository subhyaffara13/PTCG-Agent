
def _quantile_test_postprocess(res, axis, axis_none, keepdims, ndim, nan_out, xp):
    # Reshape per axis/keepdims

    res = xpx.at(res)[nan_out].set(xp.nan)

    if axis_none and keepdims:
        shape = (1,)*(ndim - 1) + res.shape
        res = xp.reshape(res, shape)
        axis = -1

    res = xp.moveaxis(res, -1, axis)

    if not keepdims:
        res = xp.squeeze(res, axis=axis)
    return res[()] if res.ndim == 0 else res

