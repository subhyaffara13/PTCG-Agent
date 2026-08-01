
def test_two_sample_tests(fun, kwargs, axis, xp):
    if fun == stats.cramervonmises_2samp and axis is None:
        pytest.skip("Sample too large for exact method.")
    mxp, marrays, narrays = get_arrays(2, xp=xp, seed=84912165484322)
    res = fun(*marrays, axis=axis, **kwargs)
    ref = fun(*narrays, nan_policy='omit', axis=axis, **kwargs)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))

