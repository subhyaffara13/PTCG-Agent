
def _quantile_iv(x, p, method, axis, nan_policy, keepdims, weights, fun='quantile'):
    xp = array_namespace(x, p, weights)

    if fun == "quantile":
        methods = {'inverted_cdf', 'averaged_inverted_cdf', 'closest_observation',
                   'hazen', 'interpolated_inverted_cdf', 'linear',
                   'median_unbiased', 'normal_unbiased', 'weibull',
                   'harrell-davis', '_lower', '_midpoint', '_higher', '_nearest',
                   'round_outward', 'round_inward', 'round_nearest'}
        allowed_types = 'real floating'
        def mask_fun(p): return (p > 1) | (p < 0) | xp.isnan(p)
        var2_name = 'p'
        var2_type_msg = '`p` must have real floating dtype.'
    else:
        methods = set(_estimated_cdf_methods)
        allowed_types = ('integral', 'real floating')
        mask_fun = xp.isnan
        var2_name = 'y'
        var2_type_msg = '`y` must have real dtype.'

    if not xp.isdtype(xp.asarray(x).dtype, ('integral', 'real floating')):
        raise ValueError("`x` must have real dtype.")

    if not xp.isdtype(xp.asarray(p).dtype, allowed_types):
        raise ValueError(var2_type_msg)

    if not (weights is None
            or xp.isdtype(xp.asarray(weights).dtype, ('integral', 'real floating'))):
        raise ValueError("`weights` must have real dtype.")

    x, p, weights = xp_promote(x, p, weights, force_floating=True, xp=xp)
    p = xp.asarray(p, device=xp_device(x))
    dtype = x.dtype

    axis_none = axis is None
    ndim = max(x.ndim, p.ndim)
    if axis_none:
        x = xp_ravel(x)
        p = xp_ravel(p)
        axis = 0
    elif np.iterable(axis) or int(axis) != axis:
        message = "`axis` must be an integer or None."
        raise ValueError(message)
    elif (axis >= ndim) or (axis < -ndim):
        message = "`axis` is not compatible with the shapes of the inputs."
        raise ValueError(message)
    axis = int(axis)

    if method not in methods:
        message = f"`method` must be one of {methods}"
        raise ValueError(message)

    no_weights = {'_lower', '_midpoint', '_higher', '_nearest', 'harrell-davis',
                  'round_nearest', 'round_inward', 'round_outward'}
    if weights is not None and method in no_weights:
        message = f"`method='{method}'` does not support `weights`."
        raise ValueError(message)

    contains_nans = _contains_nan(x, nan_policy, xp_omit_okay=True, xp=xp)

    if keepdims not in {None, True, False}:
        message = "If specified, `keepdims` must be True or False."
        raise ValueError(message)

    # If data has length zero along `axis`, the result will be an array of NaNs just
    # as if the data had length 1 along axis and were filled with NaNs. This is treated
    # naturally below whether `nan_policy` is `'propagate'` or `'omit'`.
    if x.shape[axis] == 0 and fun == 'quantile':
        shape = list(x.shape)
        shape[axis] = 1
        x = xp.full(shape, xp.nan, dtype=dtype, device=xp_device(x))

    if weights is None:
        y = xp.sort(x, axis=axis, stable=False)
        y, p = _broadcast_arrays((y, p), axis=axis)
        n_zero_weight = None
    else:
        x, weights = xp.broadcast_arrays(x, weights)
        i_zero_weight = (weights == 0)
        n_zero_weight = xp.count_nonzero(i_zero_weight, axis=axis, keepdims=True)
        x = xpx.at(x)[i_zero_weight].set(xp.inf, copy=True)
        i_y = xp.argsort(x, axis=axis, stable=False)
        y = xp.take_along_axis(x, i_y, axis=axis)
        weights = xp.take_along_axis(weights, i_y, axis=axis)
        y, p, weights, i_y, n_zero_weight = _broadcast_arrays(
            (y, p, weights, i_y, n_zero_weight), axis=axis)

    if (keepdims is False) and (p.shape[axis] != 1):
        message = ("`keepdims` may be False only if the length of "
                   f"`{var2_name}` along `axis` is 1.")
        raise ValueError(message)
    keepdims = (p.shape[axis] != 1) if keepdims is None else keepdims

    y = xp.moveaxis(y, axis, -1)
    p = xp.moveaxis(p, axis, -1)
    weights = weights if weights is None else xp.moveaxis(weights, axis, -1)
    n_zero_weight = (n_zero_weight if n_zero_weight is None
                     else xp.moveaxis(n_zero_weight, axis, -1))

    n = _count_nonmasked(y, -1, xp=xp, keepdims=True)
    n = n if n_zero_weight is None else n - n_zero_weight

    nan_out = None
    if is_lazy_array(y) or contains_nans:
        nans = xp.isnan(y)

        # Note that if length along `axis` were 0 to begin with,
        # it is now length 1 and filled with NaNs.
        if nan_policy == 'propagate':
            nan_out = xp.any(nans, axis=-1, keepdims=True)
        else:  # 'omit'
            n_int = n - xp.count_nonzero(nans, axis=-1, keepdims=True)
            n = xp.astype(n_int, dtype)
            # NaNs are produced only if slice is empty after removing NaNs
            nan_out = n == 0
            n = xpx.at(n, nan_out).set(y.shape[-1])  # avoids pytorch/pytorch#146211

        if (is_lazy_array(nans) or xp.any(nans)) and (method == 'harrell-davis'):
            y = xp.asarray(y, copy=True)  # ensure writable
            y = xpx.at(y, nans).set(0)  # any non-nan will prevent NaN from propagating
        if is_lazy_array(nan_out) or xp.any(nan_out):
            y = xp.asarray(y, copy=True)  # ensure writable
            y = xpx.at(y, xp.broadcast_to(nan_out, y.shape)).set(xp.nan)

    n = xp.asarray(n, dtype=dtype, device=xp_device(y))

    # apparently xpx.at is accepting nan_out as a mask even though it doesn't have the
    # same number of dimensions as `y`, yet it still appears to work correctly?
    # should refactor for clarity, and p_mask that gets returned here should probably
    # get a different name - `nan_out` would be more appropriate!
    p_mask = mask_fun(p) if nan_out is None else mask_fun(p) | nan_out
    if is_lazy_array(p_mask) or xp.any(p_mask):
        p = xp.where(p_mask, 0.5, p)  # these get NaN-ed out at the end

    return (y, p, method, axis, nan_policy, keepdims,
            n, axis_none, ndim, p_mask, weights, xp)

