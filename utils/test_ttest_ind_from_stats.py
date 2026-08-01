
def test_ttest_ind_from_stats(alternative, equal_var, xp):
    shape = (10, 11)
    mxp, marrays, narrays = get_arrays(6, xp=xp, shape=shape)
    mask = np.sum(np.stack([np.isnan(arg) for arg in narrays]), axis=0).astype(bool)
    narrays = [arg[~mask] for arg in narrays]
    marrays[2], marrays[5] = marrays[2] * 100, marrays[5] * 100
    narrays[2], narrays[5] = narrays[2] * 100, narrays[5] * 100

    kwargs = dict(alternative=alternative, equal_var=equal_var)
    res = stats.ttest_ind_from_stats(*marrays, **kwargs)
    ref = stats.ttest_ind_from_stats(*narrays, **kwargs)

    mask = xp.asarray(mask)
    assert xp.any(mask) and xp.any(~mask)
    xp_assert_close(res.statistic.data[~mask], xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data[~mask], xp.asarray(ref.pvalue))
    xp_assert_close(res.statistic.mask, mask)
    xp_assert_close(res.pvalue.mask, mask)
    assert res.statistic.shape == shape
    assert res.pvalue.shape == shape

