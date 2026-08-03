import math


def _boxcox_llf(data, axis=0, *, lmb):
    xp = array_namespace(data)
    dtype = xp_result_type(lmb, data, force_floating=True, xp=xp)
    data = xp.asarray(data, dtype=dtype)
    N = data.shape[axis]
    if N == 0:
        return _get_nan(data, xp=xp)

    logdata = xp.log(data)

    # Compute the variance of the transformed data.
    if lmb == 0:
        logvar = xp.log(xp.var(logdata, axis=axis))
    else:
        # Transform without the constant offset 1/lmb.  The offset does
        # not affect the variance, and the subtraction of the offset can
        # lead to loss of precision.
        # Division by lmb can be factored out to enhance numerical stability.
        logx = lmb * logdata
        logvar = _log_var(logx, xp, axis) - 2 * math.log(abs(lmb))

    res = (lmb - 1) * xp.sum(logdata, axis=axis) - N/2 * logvar
    res = xp.astype(res, data.dtype, copy=False)  # compensate for NumPy <2.0
    res = res[()] if res.ndim == 0 else res
    return res

