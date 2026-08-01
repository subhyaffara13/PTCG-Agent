
def estimated_cdf_reference(x, y, *, axis=0, nan_policy='propagate',
                        keepdims=None, method='linear'):
    x, y = _broadcast_arrays((x, y), axis=axis)
    x, y = np.moveaxis(x, axis, -1), np.moveaxis(y, axis, -1)
    res = estimated_cdf_reference_last_axis(x, y, nan_policy, method)
    res = np.moveaxis(res, -1, axis)
    if not keepdims:
        res = np.squeeze(res, axis=axis)
    return res

