
def test_wilcoxon(n_samples, zero_method, correction, alternative, method, axis, xp):
    mxp, marrays, narrays = get_arrays(n_samples, xp=xp, seed=84912165484322)
    kwargs = dict(zero_method=zero_method, correction=correction,
                  alternative=alternative, method=method)
    res = stats.wilcoxon(*marrays, axis=axis, **kwargs)
    ref = stats.wilcoxon(*narrays, nan_policy='omit', axis=axis, **kwargs)
    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))

