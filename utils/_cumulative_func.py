
def _cumulative_func(x, func, axis, dtype, out, include_initial):
    x = np.atleast_1d(x)
    x_ndim = x.ndim
    if axis is None:
        if x_ndim >= 2:
            raise ValueError("For arrays which have more than one dimension "
                            "``axis`` argument is required.")
        axis = 0

    if out is not None and include_initial:
        item = [slice(None)] * x_ndim
        item[axis] = slice(1, None)
        func.accumulate(x, axis=axis, dtype=dtype, out=out[tuple(item)])
        item[axis] = 0
        out[tuple(item)] = func.identity
        return out

    res = func.accumulate(x, axis=axis, dtype=dtype, out=out)
    if include_initial:
        initial_shape = list(x.shape)
        initial_shape[axis] = 1
        res = np.concat(
            [np.full_like(res, func.identity, shape=initial_shape), res],
            axis=axis,
        )

    return res

