
def _monte_carlo_test_iv(data, rvs, statistic, vectorized, n_resamples,
                         batch, alternative, axis):
    """Input validation for `monte_carlo_test`."""
    axis_int = int(axis)
    if axis != axis_int:
        raise ValueError("`axis` must be an integer.")

    if vectorized not in {True, False, None}:
        raise ValueError("`vectorized` must be `True`, `False`, or `None`.")

    if not isinstance(rvs, Sequence):
        rvs = (rvs,)
        data = (data,)
    for rvs_i in rvs:
        if not callable(rvs_i):
            raise TypeError("`rvs` must be callable or sequence of callables.")

    # At this point, `data` should be a sequence
    # If it isn't, the user passed a sequence for `rvs` but not `data`
    message = "If `rvs` is a sequence, `len(rvs)` must equal `len(data)`."
    try:
        len(data)
    except TypeError as e:
        raise ValueError(message) from e
    if not len(rvs) == len(data):
        raise ValueError(message)

    if not callable(statistic):
        raise TypeError("`statistic` must be callable.")

    if vectorized is None:
        try:
            signature = inspect.signature(statistic).parameters
        except ValueError as e:
            message = (f"Signature inspection of {statistic=} failed; "
                       "pass `vectorize` explicitly.")
            raise ValueError(message) from e
        vectorized = 'axis' in signature

    xp = array_namespace(*data)
    dtype = xp_result_type(*data, force_floating=True, xp=xp)

    if not vectorized:
        if is_numpy(xp):
            statistic_vectorized = _vectorize_statistic(statistic)
        else:
            message = ("`statistic` must be vectorized (i.e. support an `axis` "
                       f"argument) when `data` contains {xp.__name__} arrays.")
            raise ValueError(message)
    else:
        statistic_vectorized = statistic

    data = _broadcast_arrays(data, axis, xp=xp)
    data_iv = []
    for sample in data:
        sample = xp.broadcast_to(sample, (1,)) if sample.ndim == 0 else sample
        sample = xp.moveaxis(sample, axis_int, -1)
        data_iv.append(sample)

    n_resamples_int = int(n_resamples)
    if n_resamples != n_resamples_int or n_resamples_int <= 0:
        raise ValueError("`n_resamples` must be a positive integer.")

    if batch is None:
        batch_iv = batch
    else:
        batch_iv = int(batch)
        if batch != batch_iv or batch_iv <= 0:
            raise ValueError("`batch` must be a positive integer or None.")

    alternatives = {'two-sided', 'greater', 'less'}
    alternative = alternative.lower()
    if alternative not in alternatives:
        raise ValueError(f"`alternative` must be in {alternatives}")

    return (data_iv, rvs, statistic_vectorized, vectorized, n_resamples_int,
            batch_iv, alternative, axis_int, dtype, xp)

