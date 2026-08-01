
def _qmc_quad_iv(func, a, b, n_points, n_estimates, qrng, log, xp):
    # lazy import to avoid issues with partially-initialized submodule
    if not hasattr(qmc_quad, 'qmc'):
        from scipy import stats
        qmc_quad.stats = stats
    else:
        stats = qmc_quad.stats

    if not callable(func):
        message = "`func` must be callable."
        raise TypeError(message)

    # a, b will be modified, so copy. Oh well if it's copied twice.
    a, b = xp_promote(a, b, broadcast=True, force_floating=True, xp=xp)
    a = xpx.atleast_nd(a, ndim=1, xp=xp)
    b = xpx.atleast_nd(b, ndim=1, xp=xp)
    a, b = xp.broadcast_arrays(a, b)
    a, b = xp_copy(a), xp_copy(b)
    dim = a.shape[0]

    try:
        func((a + b) / 2)
    except Exception as e:
        message = ("`func` must evaluate the integrand at points within "
                   "the integration range; e.g. `func( (a + b) / 2)` "
                   "must return the integrand at the centroid of the "
                   "integration volume.")
        raise ValueError(message) from e

    try:
        func(xp.stack([a, b]).T)
        vfunc = func
    except Exception as e:
        if not is_numpy(xp):
            message = ("Exception encountered when attempting vectorized call to "
                       f"`func`: {e}. When using array library {xp}, `func` must "
                       "accept two-dimensional array `x` with shape `(a.shape[0], "
                       "n_points)` and return an array of the integrand value at "
                       "each of the `n_points`.")
            raise ValueError(message)

        message = ("Exception encountered when attempting vectorized call to "
                   f"`func`: {e}. For better performance, `func` should "
                   "accept two-dimensional array `x` with shape `(len(a), "
                   "n_points)` and return an array of the integrand value at "
                   "each of the `n_points`.")
        warnings.warn(message, stacklevel=3)

        def vfunc(x):
            return np.apply_along_axis(func, axis=-1, arr=x)

    n_points_int = int(n_points)
    if n_points != n_points_int:
        message = "`n_points` must be an integer."
        raise TypeError(message)

    n_estimates_int = int(n_estimates)
    if n_estimates != n_estimates_int:
        message = "`n_estimates` must be an integer."
        raise TypeError(message)

    if qrng is None:
        qrng = stats.qmc.Halton(dim)
    elif not isinstance(qrng, stats.qmc.QMCEngine):
        message = "`qrng` must be an instance of scipy.stats.qmc.QMCEngine."
        raise TypeError(message)

    if qrng.d != a.shape[0]:
        message = ("`qrng` must be initialized with dimensionality equal to "
                   "the number of variables in `a`, i.e., "
                   "`qrng.random().shape[-1]` must equal `a.shape[0]`.")
        raise ValueError(message)

    rng_seed = getattr(qrng, 'rng_seed', None)
    rng = stats._qmc.check_random_state(rng_seed)

    if log not in {True, False}:
        message = "`log` must be boolean (`True` or `False`)."
        raise TypeError(message)

    return (vfunc, a, b, n_points_int, n_estimates_int, qrng, rng, log, stats)

