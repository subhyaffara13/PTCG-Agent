
def test_slopes_intercepts(f, method, axis, xp):
    mxp, marrays, narrays = get_arrays(2, shape=(19, 20), seed=84912165484320, xp=xp)
    res = f(*marrays, axis=axis, **method)
    ref = f(*narrays, nan_policy='omit', axis=axis, **method)

    xp_assert_close(res.slope.data, xp.asarray(ref.slope))
    xp_assert_close(res.intercept.data, xp.asarray(ref.intercept))

    if f == stats.theilslopes:
        xp_assert_close(res.low_slope.data, xp.asarray(ref.low_slope))
        xp_assert_close(res.high_slope.data, xp.asarray(ref.high_slope))
    elif f == stats.linregress:
        xp_assert_close(res.rvalue.data, xp.asarray(ref.rvalue))
        xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))
        xp_assert_close(res.stderr.data, xp.asarray(ref.stderr))
        xp_assert_close(res.intercept_stderr.data, xp.asarray(ref.intercept_stderr))

