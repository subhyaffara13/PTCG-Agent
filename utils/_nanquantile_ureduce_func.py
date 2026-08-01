
def _nanquantile_ureduce_func(
        a: np.ndarray,
        q: np.ndarray,
        weights: np.ndarray,
        axis: int | None = None,
        out=None,
        overwrite_input: bool = False,
        method="linear",
        weak_q=False,
):
    """
    Private function that doesn't support extended axis or keepdims.
    These methods are extended to this function using _ureduce
    See nanpercentile for parameter usage
    """
    if axis is None or a.ndim == 1:
        part = a.ravel()
        wgt = None if weights is None else weights.ravel()
        result = _nanquantile_1d(part, q, overwrite_input, method,
                                 weights=wgt, weak_q=weak_q)
    # Note that this code could try to fill in `out` right away
    elif weights is None:
        result = np.apply_along_axis(_nanquantile_1d, axis, a, q,
                                     overwrite_input, method, weights, weak_q)
        # apply_along_axis fills in collapsed axis with results.
        # Move those axes to the beginning to match percentile's
        # convention.
        if q.ndim != 0:
            from_ax = [axis + i for i in range(q.ndim)]
            result = np.moveaxis(result, from_ax, list(range(q.ndim)))
    else:
        # We need to apply along axis over 2 arrays, a and weights.
        # move operation axes to end for simplicity:
        a = np.moveaxis(a, axis, -1)
        if weights is not None:
            weights = np.moveaxis(weights, axis, -1)
        if out is not None:
            result = out
        else:
            # weights are limited to `inverted_cdf` so the result dtype
            # is known to be identical to that of `a` here:
            result = np.empty_like(a, shape=q.shape + a.shape[:-1])

        for ii in np.ndindex(a.shape[:-1]):
            result[(...,) + ii] = _nanquantile_1d(
                    a[ii], q, weights=weights[ii],
                    overwrite_input=overwrite_input, method=method,
                    weak_q=weak_q,
            )
        # This path dealt with `out` already...
        return result

    if out is not None:
        out[...] = result
    return result

