
def test_ks_1samp(fun, method, alternative, axis, xp):
    mxp, marrays, narrays = get_arrays(1, xp=xp, seed=84912165484322)
    kwargs = dict(method=method, alternative=alternative, axis=axis)
    res = fun(*marrays, stats.norm.cdf, **kwargs)
    ref = stats.ks_1samp(*narrays, stats.norm.cdf, nan_policy='omit', **kwargs)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))
    xp_assert_equal(res.statistic_location.data, xp.asarray(ref.statistic_location))
    xp_assert_equal(res.statistic_sign.data,
                    xp.asarray(ref.statistic_sign, dtype=xp.int8))

