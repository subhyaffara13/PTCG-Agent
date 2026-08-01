
def test_correlation(f, alternative, axis, xp):
    mxp, marrays, narrays = get_arrays(2, xp=xp)

    kwargs = {} if f == stats.pointbiserialr else {'alternative': alternative}
    res = f(*marrays, **kwargs, axis=axis)

    # `pearsonr` does not have `axis_nan_policy`, so do this manually
    x, y = narrays
    if axis == 0:
        x, y = x.T, y.T
    elif axis is None:
        x, y = x.ravel()[np.newaxis, :], y.ravel()[np.newaxis, :]

    for i in range(x.shape[0]):
        xi, yi = x[i, ...], y[i, ...]
        i = () if axis is None else i

        mask = np.isnan(xi) | np.isnan(yi)
        ref = f(xi[~mask], yi[~mask], **kwargs)

        atol = 1e-7 if (is_torch(xp) and f == stats.spearmanrho) else 0.
        xp_assert_close(res.statistic.data[i], xp.asarray(ref.statistic)[()], atol=atol)
        xp_assert_close(res.pvalue.data[i], xp.asarray(ref.pvalue)[()], atol=atol)

        if f == stats.pearsonr:
            res_ci_low, res_ci_high = res.confidence_interval()
            ref_ci_low, ref_ci_high = ref.confidence_interval()
            xp_assert_close(res_ci_low.data[i], xp.asarray(ref_ci_low)[()])
            xp_assert_close(res_ci_high.data[i], xp.asarray(ref_ci_high)[()])

