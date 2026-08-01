
def _bracket_root_iv(func, xl0, xr0, xmin, xmax, factor, args, kwargs, maxiter):

    if not callable(func):
        raise ValueError('`func` must be callable.')

    if not np.iterable(args):
        args = (args,)

    xp = array_namespace(xl0, xr0, xmin, xmax, factor, *args)

    # If xr0 is not supplied, fill with a dummy value for the sake of
    # broadcasting. We need to wait until xmax has been validated to
    # compute the default value.
    xr0_not_supplied = False
    if xr0 is None:
        xr0 = xp.nan
        xr0_not_supplied = True

    xmin = -xp.inf if xmin is None else xmin
    xmax = xp.inf if xmax is None else xmax
    factor = 2. if factor is None else factor
    xl0, xr0, xmin, xmax, factor = xp_promote(
        xl0, xr0, xmin, xmax, factor, broadcast=True, force_floating=True, xp=xp)

    if not xp.isdtype(xl0.dtype, ('integral', 'real floating')):
        raise ValueError('`xl0` must be numeric and real.')

    if (not xp.isdtype(xr0.dtype, "numeric")
        or xp.isdtype(xr0.dtype, "complex floating")):
        raise ValueError('`xr0` must be numeric and real.')

    if (not xp.isdtype(xmin.dtype, "numeric")
        or xp.isdtype(xmin.dtype, "complex floating")):
        raise ValueError('`xmin` must be numeric and real.')

    if (not xp.isdtype(xmax.dtype, "numeric")
        or xp.isdtype(xmax.dtype, "complex floating")):
        raise ValueError('`xmax` must be numeric and real.')

    if (not xp.isdtype(factor.dtype, "numeric")
        or xp.isdtype(factor.dtype, "complex floating")):
        raise ValueError('`factor` must be numeric and real.')
    if not xp.all(factor > 1):
        raise ValueError('All elements of `factor` must be greater than 1.')

    # Calculate the default value of xr0 if a value has not been supplied.
    # Be careful to ensure xr0 is not larger than xmax.
    if xr0_not_supplied:
        xr0 = xl0 + xp.minimum((xmax - xl0)/ 8, xp.ones_like(xmax))
        xr0 = xp.astype(xr0, xl0.dtype, copy=False)

    maxiter = xp.asarray(maxiter)
    message = '`maxiter` must be a non-negative integer.'
    if (not xp.isdtype(maxiter.dtype, "numeric") or maxiter.shape != tuple()
            or xp.isdtype(maxiter.dtype, "complex floating")):
        raise ValueError(message)
    maxiter_int = int(maxiter[()])
    if not maxiter == maxiter_int or maxiter < 0:
        raise ValueError(message)

    return func, xl0, xr0, xmin, xmax, factor, args, kwargs, maxiter, xp

