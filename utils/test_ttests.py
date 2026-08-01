
def test_ttests(f, alternative, axis, xp):
    f_name = f.__name__
    mxp, marrays, narrays = get_arrays(2, xp=xp)
    if f_name == 'ttest_1samp':
        marrays[1] = mxp.mean(marrays[1], axis=axis, keepdims=axis is not None)
        narrays[1] = np.nanmean(narrays[1], axis=axis, keepdims=axis is not None)
    res = f(*marrays, alternative=alternative, axis=axis)
    ref = f(*narrays, alternative=alternative, nan_policy='omit', axis=axis)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))
    res_ci = res.confidence_interval()
    ref_ci = ref.confidence_interval()
    xp_assert_close(res_ci.low.data, xp.asarray(ref_ci.low))
    xp_assert_close(res_ci.high.data, xp.asarray(ref_ci.high))

