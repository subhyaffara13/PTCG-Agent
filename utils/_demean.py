
def _demean(a, mean, axis, *, xp, precision_warning=True):
    # subtracts `mean` from `a` and returns the result,
    # warning if there is catastrophic cancellation. `mean`
    # must be the mean of `a` along axis with `keepdims=True`.
    # Used in e.g. `_moment`, `_zscore`, `_xp_var`. See gh-15905.
    a_zero_mean = a - mean

    if (xp_size(a_zero_mean) == 0 or not precision_warning
        or is_lazy_array(a_zero_mean)):
        return a_zero_mean

    eps = xp.finfo(mean.dtype).eps * 10

    with np.errstate(divide='ignore', invalid='ignore'):
        rel_diff = xp.max(xp.abs(a_zero_mean), axis=axis,
                          keepdims=True) / xp.abs(mean)

    n = _count_nonmasked(a, axis, xp=xp)
    with np.errstate(invalid='ignore'):
        device = {'device': xp_device(a)}
        precision_loss = xp.any(xp.asarray(rel_diff < eps, **device)
                                & xp.asarray(n > 1, **device))

    if precision_loss:
        message = ("Precision loss occurred in moment calculation due to "
                   "catastrophic cancellation. This occurs when the data "
                   "are nearly identical. Results may be unreliable.")
        warnings.warn(message, RuntimeWarning, stacklevel=5)
    return a_zero_mean

