
def _continued_fraction_iv(a, b, args, tolerances, maxiter, log):
    # Input validation for `_continued_fraction`

    if not callable(a) or not callable(b):
        raise ValueError('`a` and `b` must be callable.')

    if not np.iterable(args):
        args = (args,)

    # Call each callable once to determine namespace and dtypes
    a0, b0 = a(0, *args), b(0, *args)
    xp = array_namespace(a0, b0, *args)
    a0, b0, *args = xp_promote(a0, b0, *args, force_floating=True, broadcast=True,
                               xp=xp)
    shape, dtype = a0.shape, a0.dtype
    a0, b0, *args = (xp_ravel(arg) for arg in (a0, b0) + tuple(args))

    tolerances = {} if tolerances is None else tolerances
    eps = tolerances.get('eps', None)
    tiny = tolerances.get('tiny', None)

    # tolerances are floats, not arrays, so it's OK to use NumPy
    message = ('`eps` and `tiny` must be (or represent the logarithm of) '
               'finite, positive, real scalars.')
    tols = np.asarray([eps if eps is not None else 1,
                       tiny if tiny is not None else 1])
    not_real = (not np.issubdtype(tols.dtype, np.number)
                or np.issubdtype(tols.dtype, np.complexfloating))
    not_positive = np.any(tols <= 0) if not log else False
    not_finite = not np.all(np.isfinite(tols))
    not_scalar = tols.shape != (2,)
    if not_real or not_positive or not_finite or not_scalar:
        raise ValueError(message)

    maxiter_int = int(maxiter)
    if maxiter != maxiter_int or maxiter < 0:
        raise ValueError('`maxiter` must be a non-negative integer.')

    if not isinstance(log, bool):
        raise ValueError('`log` must be boolean.')

    return a, b, args, eps, tiny, maxiter, log, a0, b0, shape, dtype, xp

