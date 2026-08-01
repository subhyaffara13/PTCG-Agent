
def _bracket_minimum_iv(func, xm0, xl0, xr0, xmin, xmax, factor, args, kwargs, maxiter):

    if not callable(func):
        raise ValueError('`func` must be callable.')

    if not np.iterable(args):
        args = (args,)

    xp = array_namespace(xm0, xl0, xr0, xmin, xmax, factor, *args)

    xmin = -xp.inf if xmin is None else xmin
    xmax = xp.inf if xmax is None else xmax

    # If xl0 (xr0) is not supplied, fill with a dummy value for the sake
    # of broadcasting. We need to wait until xmin (xmax) has been validated
    # to compute the default values.
    xl0_not_supplied = False
    if xl0 is None:
        xl0 = xp.nan
        xl0_not_supplied = True

    xr0_not_supplied = False
    if xr0 is None:
        xr0 = xp.nan
        xr0_not_supplied = True

    factor = 2.0 if factor is None else factor

    xm0, xl0, xr0, xmin, xmax, factor = xp_promote(
        xm0, xl0, xr0, xmin, xmax, factor, broadcast=True, force_floating=True, xp=xp)

    if not xp.isdtype(xm0.dtype, ('integral', 'real floating')):
        raise ValueError('`xm0` must be numeric and real.')

    if (not xp.isdtype(xl0.dtype, "numeric")
        or xp.isdtype(xl0.dtype, "complex floating")):
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

    # Calculate default values of xl0 and/or xr0 if they have not been supplied
    # by the user. We need to be careful to ensure xl0 and xr0 are not outside
    # of (xmin, xmax).
    if xl0_not_supplied:
        xl0 = xm0 - xp.minimum((xm0 - xmin)/16, 0.5)
        xl0 = xp.astype(xl0, xm0.dtype, copy=False)
    if xr0_not_supplied:
        xr0 = xm0 + xp.minimum((xmax - xm0)/16, 0.5)
        xr0 = xp.astype(xr0, xm0.dtype, copy=False)

    maxiter = xp.asarray(maxiter)
    message = '`maxiter` must be a non-negative integer.'
    if (not xp.isdtype(maxiter.dtype, "numeric") or maxiter.shape != tuple()
            or xp.isdtype(maxiter.dtype, "complex floating")):
        raise ValueError(message)
    maxiter_int = int(maxiter[()])
    if not maxiter == maxiter_int or maxiter < 0:
        raise ValueError(message)

    return func, xm0, xl0, xr0, xmin, xmax, factor, args, kwargs, maxiter, xp

