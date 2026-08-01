
def _xp_obrientransform_one_sample(a, *, xp, nan_policy):
    _contains_nan(a, nan_policy, xp_omit_okay=True)  # handle `nan_policy='raise'`
    n = xp.asarray(xp.count_nonzero(~xp.isnan(a)), dtype=a.dtype)
    mu = _xp_mean(a, nan_policy=nan_policy)
    sq = (a - mu)**2
    sumsq = _xp_mean(sq, nan_policy=nan_policy) * n
    return ((n - 1.5) * n * sq - 0.5 * sumsq) / ((n - 1) * (n - 2))

