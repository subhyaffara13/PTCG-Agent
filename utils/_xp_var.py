
def _xp_var(x, /, *, axis=None, correction=0, keepdims=False, nan_policy='propagate',
            dtype=None, xp=None):
    # an array-api compatible function for variance with scipy.stats interface
    # and features (e.g. `nan_policy`).
    xp = array_namespace(x) if xp is None else xp
    x = _asarray(x, subok=True)

    # use `_xp_mean` instead of `xp.var` for desired warning behavior
    # it would be nice to combine this with `_var`, which uses `_moment`
    # and therefore warns when precision is lost, but that does not support
    # `axis` tuples or keepdims. Eventually, `_axis_nan_policy` will simplify
    # `axis` tuples and implement `keepdims` for non-NumPy arrays; then it will
    # be easy.
    kwargs = dict(axis=axis, nan_policy=nan_policy, dtype=dtype, xp=xp)
    mean = _xp_mean(x, keepdims=True, **kwargs)
    x = _asarray(x, dtype=mean.dtype, subok=True)
    x_mean = _demean(x, mean, axis, xp=xp)
    x_mean_conj = (xp.conj(x_mean) if xp.isdtype(x_mean.dtype, 'complex floating')
                   else x_mean)  # crossref data-apis/array-api#824
    var = _xp_mean(x_mean * x_mean_conj, keepdims=keepdims, **kwargs)

    if correction != 0:
        n = _count_nonmasked(x, axis, xp=xp, keepdims=keepdims)
        # Or two lines with ternaries : )
        # axis = range(x.ndim) if axis is None else axis
        # n = math.prod(x.shape[i] for i in axis) if iterable(axis) else x.shape[axis]

        n = xp.asarray(n, dtype=var.dtype, device=xp_device(x))

        if nan_policy == 'omit':
            nan_mask = xp.astype(xp.isnan(x), var.dtype)
            n = n - xp.sum(nan_mask, axis=axis, keepdims=keepdims)

        # Produce NaNs silently when n - correction <= 0
        nc = n - correction
        factor = xpx.apply_where(nc > 0, (n, nc), operator.truediv, fill_value=xp.nan)
        var *= factor

    return var[()] if var.ndim == 0 else var

