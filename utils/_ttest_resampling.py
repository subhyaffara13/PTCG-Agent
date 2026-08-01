
def _ttest_resampling(x, y, axis, alternative, ttest_kwargs, method, *, xp):
    def statistic(x, y, axis):
        x, y = xp.asarray(x), xp.asarray(y)
        return ttest_ind(x, y, axis=axis, **ttest_kwargs).statistic

    test = (permutation_test if isinstance(method, PermutationMethod)
            else monte_carlo_test)
    method = method._asdict()

    if test is monte_carlo_test:
        # `monte_carlo_test` accepts an `rvs` tuple of callables, not an `rng`
        # If the user specified an `rng`, replace it with the default callables
        if (rng := method.pop('rng', None)) is not None:
            rng = np.random.default_rng(rng)
            method['rvs'] = rng.normal, rng.normal

    res = test((x, y,), statistic=statistic, axis=axis,
               alternative=alternative, **method)

    return res.statistic, res.pvalue

