
def test_power_divergence_chisquare(f, lambda_, ddof, axis, xp):
    mxp, marrays, narrays = get_arrays(2, xp=xp, shape=(5, 6))

    kwargs = dict(axis=axis, ddof=ddof)

    # test 1-arg
    res = f(marrays[0], **lambda_, **kwargs)
    ref = stats.power_divergence(narrays[0], nan_policy='omit', **lambda_, **kwargs)

    xp_assert_close(res.statistic.data, xp.asarray(ref[0]))
    xp_assert_close(res.pvalue.data, xp.asarray(ref[1]))

    # test 2-arg
    common_mask = np.isnan(narrays[0]) | np.isnan(narrays[1])
    normalize = (np.nansum(narrays[1] * ~common_mask, axis=axis, keepdims=True)
                 / np.nansum(narrays[0] * ~common_mask, axis=axis, keepdims=True))
    marrays[0] *= xp.asarray(normalize)
    narrays[0] *= normalize

    res = f(*marrays, **lambda_, **kwargs)
    ref = stats.power_divergence(*narrays, nan_policy='omit', **lambda_, **kwargs)

    xp_assert_close(res.statistic.data, xp.asarray(ref[0]))
    xp_assert_close(res.pvalue.data, xp.asarray(ref[1]))

