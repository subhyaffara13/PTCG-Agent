
def test_goodness_of_fit(f, args, alternative, axis, xp):
    mxp, marrays, narrays = get_arrays(1, xp=xp, shape=(10, 11))

    if f in {stats.skewtest, stats.kurtosistest}:
        kwds = {'alternative': alternative}
    else:
        if alternative != 'greater':
            pytest.skip(f'str({f.__name__} does not support multiple alternatives.')
        kwds = {}

    res = f(*marrays, *args, **kwds, axis=axis)
    ref = f(*narrays, *args, **kwds, nan_policy='omit', axis=axis)

    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue), atol=1e-15)

