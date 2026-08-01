
def _tanhsinh_iv(f, a, b, log, maxfun, maxlevel, minlevel,
                 atol, rtol, args, kwargs, preserve_shape, callback):
    # Input validation and standardization

    xp = array_namespace(a, b)
    a, b = xp_promote(a, b, broadcast=True, force_floating=True, xp=xp)

    message = '`f` must be callable.'
    if not callable(f):
        raise ValueError(message)

    message = 'All elements of `a` and `b` must be real numbers.'
    if (xp.isdtype(a.dtype, 'complex floating')
            or xp.isdtype(b.dtype, 'complex floating')):
        raise ValueError(message)

    message = '`log` must be True or False.'
    if log not in {True, False}:
        raise ValueError(message)
    log = bool(log)

    if atol is None:
        atol = -xp.inf if log else 0

    rtol_temp = rtol if rtol is not None else 0.

    # using NumPy for convenience here; these are just floats, not arrays
    params = np.asarray([atol, rtol_temp, 0.])
    message = "`atol` and `rtol` must be real numbers."
    if not np.issubdtype(params.dtype, np.floating):
        raise ValueError(message)

    if log:
        message = '`atol` and `rtol` may not be positive infinity.'
        if np.any(np.isposinf(params)):
            raise ValueError(message)
    else:
        message = '`atol` and `rtol` must be non-negative and finite.'
        if np.any(params < 0) or np.any(np.isinf(params)):
            raise ValueError(message)
    atol = params[0]
    rtol = rtol if rtol is None else params[1]

    BIGINT = float(2**62)
    if maxfun is None and maxlevel is None:
        maxlevel = 10

    maxfun = BIGINT if maxfun is None else maxfun
    maxlevel = BIGINT if maxlevel is None else maxlevel

    message = '`maxfun`, `maxlevel`, and `minlevel` must be integers.'
    params = np.asarray([maxfun, maxlevel, minlevel])
    if not (np.issubdtype(params.dtype, np.number)
            and np.all(np.isreal(params))
            and np.all(params.astype(np.int64) == params)):
        raise ValueError(message)
    message = '`maxfun`, `maxlevel`, and `minlevel` must be non-negative.'
    if np.any(params < 0):
        raise ValueError(message)
    maxfun, maxlevel, minlevel = params.astype(np.int64)
    minlevel = min(minlevel, maxlevel)

    if not np.iterable(args):
        args = (args,)

    message = '`preserve_shape` must be True or False.'
    if preserve_shape not in {True, False}:
        raise ValueError(message)

    if callback is not None and not callable(callback):
        raise ValueError('`callback` must be callable.')

    return (f, a, b, log, maxfun, maxlevel, minlevel,
            atol, rtol, args, kwargs, preserve_shape, callback, xp)

