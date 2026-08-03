import math


def _permutation_test_iv(data, statistic, permutation_type, vectorized,
                         n_resamples, batch, alternative, axis, rng):
    """Input validation for `permutation_test`."""
    axis_int = int(axis)
    if axis != axis_int:
        raise ValueError("`axis` must be an integer.")

    permutation_types = {'samples', 'pairings', 'independent'}
    permutation_type = permutation_type.lower()
    if permutation_type not in permutation_types:
        raise ValueError(f"`permutation_type` must be in {permutation_types}.")

    if vectorized not in {True, False, None}:
        raise ValueError("`vectorized` must be `True`, `False`, or `None`.")

    if vectorized is None:
        vectorized = 'axis' in inspect.signature(statistic).parameters

    message = "`data` must be a tuple containing at least two samples"
    try:
        if len(data) < 2 and permutation_type == 'independent':
            raise ValueError(message)
    except TypeError:
        raise TypeError(message)

    xp = array_namespace(*data)

    if not vectorized:
        if not is_numpy(xp):
            message = (f"When using array library {xp.__name__}, `func` must be "
                       "vectorized and accept argument `axis`.")
            raise TypeError(message)

        statistic = _vectorize_statistic(statistic)

    data = _broadcast_arrays(data, axis, xp=xp)
    data_iv = []
    for sample in data:
        sample = xpx.atleast_nd(sample, ndim=1)
        if sample.shape[axis] <= 1:
            raise ValueError("each sample in `data` must contain two or more "
                             "observations along `axis`.")
        sample = xp.moveaxis(sample, axis_int, -1)
        data_iv.append(sample)

    n_resamples_int = (int(n_resamples) if not math.isinf(n_resamples)
                       else xp.inf)
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

    rng = check_random_state(rng)

    float_dtype = xp_result_type(*data_iv, force_floating=True, xp=xp)

    return (data_iv, statistic, permutation_type, vectorized, n_resamples_int,
            batch_iv, alternative, axis_int, rng, float_dtype, xp)

