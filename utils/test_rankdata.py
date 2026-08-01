
def test_rankdata(method, axis, xp):
    mxp, marrays, narrays = get_arrays(1, xp=xp)
    res = stats.rankdata(*marrays, method=method, axis=axis)
    ref = stats.rankdata(*narrays, method=method, nan_policy='omit', axis=axis)
    xp_assert_close(res.data[~res.mask], xp.asarray(ref[~np.isnan(ref)]))
    xp_assert_close(res.mask, xp.asarray(np.isnan(ref)))

