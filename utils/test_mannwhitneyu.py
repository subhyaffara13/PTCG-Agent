
def test_mannwhitneyu(use_continuity, alternative, method, axis, xp):
    mxp, marrays, narrays = get_arrays(2, xp=xp, seed=84912165484322)
    kwargs = dict(use_continuity=use_continuity, alternative=alternative, method=method)
    res = stats.mannwhitneyu(*marrays, axis=axis, **kwargs)
    ref = stats.mannwhitneyu(*narrays, nan_policy='omit', axis=axis, **kwargs)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))

