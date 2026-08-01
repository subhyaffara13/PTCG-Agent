
def check_equal_xmean(*args, xp, mean_fun, axis=None, dtype=None,
                      rtol=None, weights=None):
    # Note this doesn't test when axis is not specified
    dtype = dtype or xp.float64
    if len(args) == 2:
        array_like, desired = args
    else:
        array_like, p, desired = args
    array_like = xp.asarray(array_like, dtype=dtype)
    dtype_reference = (xp_result_type(array_like, force_floating=True, xp=xp)
                       if xp != np.ma else None)
    desired = xp.asarray(desired, dtype=dtype_reference)
    weights = xp.asarray(weights, dtype=dtype) if weights is not None else weights
    args = (array_like,) if len(args) == 2 else (array_like, p)
    x = mean_fun(*args, axis=axis, weights=weights)
    xp_assert_close(x, desired, rtol=rtol)

