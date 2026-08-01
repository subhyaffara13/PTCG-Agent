
def _weight_masked(arrays, weights, axis):
    if axis is None:
        axis = 0
    weights = np.asanyarray(weights)
    for a in arrays:
        axis_mask = np.ma.getmask(a)
        if axis_mask is np.ma.nomask:
            continue
        if a.ndim > 1:
            not_axes = tuple(i for i in range(a.ndim) if i != axis)
            axis_mask = axis_mask.any(axis=not_axes)
        weights *= 1 - axis_mask.astype(int)
    return weights

