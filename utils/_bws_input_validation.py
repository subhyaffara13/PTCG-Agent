
def _bws_input_validation(x, y, alternative, axis, method):
    ''' Input validation and standardization for bws test'''
    xp = array_namespace(x, y)
    x, y = xp.asarray(x), xp.asarray(y)
    x, y = xpx.atleast_nd(x, ndim=1), xpx.atleast_nd(y, ndim=1)

    axis_none = axis is None
    ndim = max(x.ndim, y.ndim)
    if axis_none:
        x = xp_ravel(x, xp=xp)
        y = xp_ravel(y, xp=xp)
        axis = 0
    elif np.iterable(axis) or int(axis) != axis:
        message = "`axis` must be an integer or None."
        raise ValueError(message)
    elif (axis >= ndim) or (axis < -ndim):
        message = "`axis` is not compatible with the shapes of the inputs."
        raise ValueError(message)
    axis = int(axis)

    x, y = _broadcast_arrays((x, y), axis=axis, xp=xp)
    nx, ny = x.shape[-1], y.shape[-1]
    if nx < 2 or ny < 2:
        raise ValueError('`x` and `y` must contain at least two observations each.')

    x, y = xp.moveaxis(x, axis, -1), xp.moveaxis(y, axis, -1)
    z = stats.rankdata(xp.concat((x, y), axis=-1), axis=-1)
    z = xp.astype(z, xp_result_type(x, y, force_floating=True, xp=xp))
    x, y = z[..., :x.shape[-1]], z[..., x.shape[-1]:]
    x, y = xp.moveaxis(x, -1, axis), xp.moveaxis(y, -1, axis)

    alternatives = {'two-sided', 'less', 'greater'}
    alternative = alternative.lower()
    if alternative not in alternatives:
        raise ValueError(f'`alternative` must be one of {alternatives}.')

    method = stats.PermutationMethod() if method is None else method
    if not isinstance(method, stats.PermutationMethod):
        raise ValueError('`method` must be an instance of '
                         '`scipy.stats.PermutationMethod`')

    return x, y, alternative, axis, method, xp

