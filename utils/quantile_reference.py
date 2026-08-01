
def quantile_reference(x, p, *, axis, nan_policy, keepdims, method):
    x, p = np.moveaxis(x, axis, -1), np.moveaxis(np.atleast_1d(p), axis, -1)
    res = quantile_reference_last_axis(x, p, nan_policy, method)
    res = np.moveaxis(res, -1, axis)
    if not keepdims:
        res = np.squeeze(res, axis=axis)
    return res

