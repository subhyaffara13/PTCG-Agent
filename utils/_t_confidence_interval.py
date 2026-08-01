
def _t_confidence_interval(df, t, confidence_level, alternative, dtype=None, xp=None):
    # Input validation on `alternative` is already done
    # We just need IV on confidence_level
    dtype = t.dtype if dtype is None else dtype
    xp = array_namespace(t) if xp is None else xp

    if confidence_level < 0 or confidence_level > 1:
        message = "`confidence_level` must be a number between 0 and 1."
        raise ValueError(message)

    confidence_level = xp.asarray(confidence_level, dtype=dtype, device=xp_device(t))
    inf = xp.asarray(xp.inf, dtype=dtype)

    if alternative < 0:  # 'less'
        p = confidence_level
        low, high = xp.broadcast_arrays(-inf, special.stdtrit(df, p))
    elif alternative > 0:  # 'greater'
        p = 1 - confidence_level
        low, high = xp.broadcast_arrays(special.stdtrit(df, p), inf)
    elif alternative == 0:  # 'two-sided'
        tail_probability = (1 - confidence_level)/2
        p = xp.stack((tail_probability, 1-tail_probability))
        # axis of p must be the zeroth and orthogonal to all the rest
        p = xp.reshape(p, tuple([2] + [1]*xp.asarray(df, device=xp_device(t)).ndim))
        ci = special.stdtrit(df, p)
        low, high = ci[0, ...], ci[1, ...]
    else:  # alternative is NaN when input is empty (see _axis_nan_policy)
        nan = xp.asarray(xp.nan, device=xp_device(t))
        p, nans = xp.broadcast_arrays(t, nan)
        low, high = nans, nans

    low = xp.asarray(low, dtype=dtype)
    low = low[()] if low.ndim == 0 else low
    high = xp.asarray(high, dtype=dtype)
    high = high[()] if high.ndim == 0 else high
    return low, high

