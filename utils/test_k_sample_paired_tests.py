
def test_k_sample_paired_tests(fun, kwargs, axis, xp):
    mxp, marrays, narrays = get_arrays(3, shape=(8, 9), xp=xp)
    res = fun(*marrays, axis=axis, **kwargs)
    ref = fun(*narrays, nan_policy='omit', axis=axis, **kwargs)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))

