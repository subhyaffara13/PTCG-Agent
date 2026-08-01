
def test_parameter_vectorized(fun_name):
    # Check that parameter `vectorized` is working as desired for all
    # resampling functions. Results don't matter; just don't fail asserts.
    rng = np.random.default_rng(75245098234592)
    sample = rng.random(size=10)

    def rvs(size):  # needed by `monte_carlo_test`
        return stats.norm.rvs(size=size, random_state=rng)

    fun_options = {'bootstrap': {'data': (sample,), 'rng': rng,
                                 'method': 'percentile'},
                   'permutation_test': {'data': (sample,), 'rng': rng,
                                        'permutation_type': 'samples'},
                   'monte_carlo_test': {'sample': sample, 'rvs': rvs}}
    common_options = {'n_resamples': 100}

    fun = getattr(stats, fun_name)
    options = fun_options[fun_name]
    options.update(common_options)

    def statistic(x, axis):
        assert x.ndim > 1 or np.array_equal(x, sample)
        return np.mean(x, axis=axis)
    fun(statistic=statistic, vectorized=None, **options)
    fun(statistic=statistic, vectorized=True, **options)

    def statistic(x):
        assert x.ndim == 1
        return np.mean(x)
    fun(statistic=statistic, vectorized=None, **options)
    fun(statistic=statistic, vectorized=False, **options)

