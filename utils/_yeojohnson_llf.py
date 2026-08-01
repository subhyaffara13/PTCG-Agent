
def _yeojohnson_llf(data, *, lmb, axis=0):
    xp = array_namespace(data)
    dtype = xp_result_type(lmb, data, force_floating=True, xp=xp)
    data = xp.asarray(data, dtype=dtype)

    n = data.shape[axis]
    if n == 0:
        return _get_nan(data, xp=xp)
    eps = xp.finfo(dtype).eps
    # Special case all-positive/negative data to avoid overflow and precision loss
    pos = data >= 0  # binary mask

    # There exists numerical instability when abs(lmb) or abs(lmb - 2) is very small
    if not is_lazy_array(pos) and xp.all(pos):
        if abs(lmb) < eps:
            logvar = xp.log(xp.var(xp.log1p(data), axis=axis))
        else:
            logvar = _log_var(lmb * xp.log1p(data), xp, axis) - 2 * math.log(abs(lmb))

    elif not is_lazy_array(pos) and xp.all(~pos):
        if abs(lmb - 2) < eps:
            logvar = xp.log(xp.var(xp.log1p(-data), axis=axis))
        else:
            logvar = _log_var((2 - lmb) * xp.log1p(-data), xp, axis) - 2 * math.log(
                abs(2 - lmb)
            )

    # overflow/precision loss not reported for mixed data; calculate `logvar` directly
    else:  # mixed positive and negative data
        y = _yeojohnson_transform(data, lmb, xp=xp)
        sigma = xp.var(y, axis=axis)

        # Suppress RuntimeWarning raised by np.log when the variance is too low
        finite_variance = sigma >= xp.finfo(sigma.dtype).smallest_normal
        logvar = xpx.apply_where(finite_variance, (sigma,), xp.log, fill_value=-xp.inf)

    loglike = (-n / 2 * logvar
               + (lmb - 1) * xp.sum(xp.sign(data) * xp.log1p(xp.abs(data)), axis=axis))

    return loglike

