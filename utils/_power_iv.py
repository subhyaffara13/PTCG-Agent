
def _power_iv(rvs, test, n_observations, significance, vectorized,
              n_resamples, batch, kwargs):
    """Input validation for `monte_carlo_test`."""
    if vectorized not in {True, False, None}:
        raise ValueError("`vectorized` must be `True`, `False`, or `None`.")

    if not isinstance(rvs, Sequence):
        rvs = (rvs,)
        n_observations = (n_observations,)
    for rvs_i in rvs:
        if not callable(rvs_i):
            raise TypeError("`rvs` must be callable or sequence of callables.")

    if not len(rvs) == len(n_observations):
        message = ("If `rvs` is a sequence, `len(rvs)` "
                   "must equal `len(n_observations)`.")
        raise ValueError(message)

    kwargs = dict() if kwargs is None else kwargs
    if not isinstance(kwargs, dict):
        raise TypeError("`kwargs` must be a dictionary that maps keywords to arrays.")

    vals = kwargs.values()
    keys = kwargs.keys()

    xp = array_namespace(*n_observations, significance, *vals)

    significance = xp.asarray(significance)
    if not xp.isdtype(significance.dtype, "real floating"):
        raise ValueError("`significance` must be of floating point dtype.")

    if is_lazy_array(significance):
        significance = xp.where((significance < 0.) | (significance > 1.),
                                xp.nan, significance)
    elif xp.min(significance) < 0. or xp.max(significance) > 1.:
        raise ValueError("All elements of `significance` must be between 0. and 1.")

    # Wrap callables to ignore unused keyword arguments
    wrapped_rvs = [_wrap_kwargs(rvs_i) for rvs_i in rvs]

    # Broadcast, then ravel nobs/kwarg combinations. In the end,
    # `nobs` and `vals` have shape (# of combinations, number of variables)
    # todo: find a better way to do this without combining arrays
    tmp = xp.stack(xp.broadcast_arrays(*n_observations, *vals))
    shape = tmp.shape
    if tmp.ndim == 1:
        tmp = xp.expand_dims(tmp, axis=0)
    else:
        tmp = xp.reshape(tmp, (shape[0], -1)).T
    nobs, vals = tmp[:, :len(rvs)], tmp[:, len(rvs):]
    integer_dtype = xp_result_type(*n_observations, xp=xp)
    nobs = xp.astype(nobs, integer_dtype)

    if not callable(test):
        raise TypeError("`test` must be callable.")

    if vectorized is None:
        vectorized = 'axis' in inspect.signature(test).parameters

    test_vectorized = test
    if not vectorized:
        if not is_numpy(xp):
            message = (f"When using array library {xp.__name__}, `test` must be "
                       "be vectorized and accept argument `axis`.")
            raise TypeError(message)

        test_vectorized = _vectorize_statistic(test)

    # Wrap `test` function to ignore unused kwargs
    test_vectorized = _wrap_kwargs(test_vectorized)

    n_resamples_int = int(n_resamples)
    if n_resamples != n_resamples_int or n_resamples_int <= 0:
        raise ValueError("`n_resamples` must be a positive integer.")

    if batch is None:
        batch_iv = batch
    else:
        batch_iv = int(batch)
        if batch != batch_iv or batch_iv <= 0:
            raise ValueError("`batch` must be a positive integer or None.")

    return (wrapped_rvs, test_vectorized, nobs, significance, vectorized,
            n_resamples_int, batch_iv, vals, keys, shape[1:], xp)

