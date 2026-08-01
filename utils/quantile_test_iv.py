
def quantile_test_iv(x, q, p, alternative, axis, keepdims):
    xp = array_namespace(x, q, p)
    dtype = xp_result_type(x, q, p, force_floating=True, xp=xp)

    x = xpx.atleast_nd(x, ndim=1, xp=xp)
    message = '`x` must be an array of numbers.'
    if not xp.isdtype(x.dtype, 'numeric'):
        raise ValueError(message)

    q = xp.asarray(q)
    message = "`q` must be a scalar or array of numbers."
    if not xp.isdtype(q.dtype, 'numeric'):
        raise ValueError(message)

    p = xp.asarray(p)
    message = "`p` must be a scalar or array of floats."
    if not xp.isdtype(p.dtype, 'real floating'):
        raise ValueError(message)

    axis_none = axis is None
    ndim = max(x.ndim, p.ndim)
    if axis_none:
        x = xp_ravel(x)
        q = xp_ravel(q)
        p = xp_ravel(p)
        axis = 0
    elif np.iterable(axis) or int(axis) != axis:
        message = "`axis` must be an integer or None."
        raise ValueError(message)
    elif (axis >= ndim) or (axis < -ndim):
        message = "`axis` is not compatible with the shapes of the inputs."
        raise ValueError(message)
    axis = int(axis)

    alternatives = {'two-sided', 'less', 'greater'}
    message = f"`alternative` must be one of {alternatives}"
    if alternative not in alternatives:
        raise ValueError(message)

    if keepdims not in {None, True, False}:
        message = "If specified, `keepdims` must be True or False."
        raise ValueError(message)

    x = xp.sort(x, axis=axis)
    q, p = xp.broadcast_arrays(q, p)  # length along axis matters for q and p
    x, q, p = _broadcast_arrays((x, q, p), axis=axis, xp=xp)

    if (keepdims is False) and (p.shape[axis] != 1):
        message = ("`keepdims` may be False only if `p` and `q` are scalars or the "
                   "length of `p` and `q` along `axis` is 1.")
        raise ValueError(message)
    keepdims = (p.shape[axis] != 1) if keepdims is None else keepdims

    x = xp.moveaxis(x, axis, -1)
    q = xp.moveaxis(q, axis, -1)
    p = xp.moveaxis(p, axis, -1)

    nan_out = ((p >= 1) | (p <= 0) | xp.isnan(p) | xp.isnan(q)
               | xp.any(xp.isnan(x), axis=-1, keepdims=True))
    if is_lazy_array(nan_out) or xp.any(nan_out):
        # These get NaN-ed out at the end. In the meantime, we want them
        # to pass through calculations without warnings or errors
        q = xpx.at(q, nan_out).set(0.0, copy=True)
        p = xpx.at(p, nan_out).set(0.5, copy=True)

    return x, q, p, alternative, axis, keepdims, axis_none, ndim, nan_out, dtype, xp

