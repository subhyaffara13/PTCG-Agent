
def test_ks_2samp(fun, method, alternative, axis, xp):
    mxp, marrays, narrays = get_arrays(2, xp=xp, seed=84912165484322)
    kwargs = dict(method=method, alternative=alternative, axis=axis)
    res = fun(*marrays, **kwargs)
    ref = stats.ks_2samp(*narrays, nan_policy='omit', **kwargs)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))
    # with this random data, there often multiple locations where the statistic assumes
    # the most extreme value, so we can't expect these to always match
    # xp_assert_equal(res.statistic_location.data, xp.asarray(ref.statistic_location))
    xp_assert_equal(res.statistic_sign.data,
                    xp.asarray(ref.statistic_sign, dtype=xp.int8))

