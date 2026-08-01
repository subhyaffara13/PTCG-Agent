
def test_one_sample_non_reducing(fun, ddof, axis, xp):
    mxp, marrays, narrays = (get_arrays(2, xp=xp) if fun == stats.zmap
                             else get_arrays(1, xp=xp))
    res = fun(*marrays, ddof=ddof, axis=axis)
    ref = xp.asarray(fun(*narrays, ddof=ddof, nan_policy='omit', axis=axis))
    xp_assert_close(res.data[~res.mask], ref[~xp.isnan(ref)])
    xp_assert_equal(res.mask, marrays[0].mask)

