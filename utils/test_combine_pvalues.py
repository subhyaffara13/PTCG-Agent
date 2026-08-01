
def test_combine_pvalues(method, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        pvalues = get_arrays(1, xp=xp, dtype=dtype, device=device)[0] / 10
        res = stats.combine_pvalues(pvalues, method=method)
        assert xp_device(res.statistic) == xp_device(pvalues)
        assert xp_device(res.pvalue) == xp_device(pvalues)
        assert res.statistic.dtype == dtype
        assert res.pvalue.dtype == dtype


def test_combine_pvalues(method, axis, xp):
    mxp, marrays, narrays = get_arrays(2, xp=xp, shape=(10, 11))

    kwargs = dict(method=method, axis=axis)
    res = stats.combine_pvalues(marrays[0], **kwargs)
    ref = stats.combine_pvalues(narrays[0], nan_policy='omit', **kwargs)

    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))

    if method != 'stouffer':
        return

    # test method='stouffer' with weights
    res = stats.combine_pvalues(marrays[0], weights=marrays[1], **kwargs)
    ref = stats.combine_pvalues(narrays[0], weights=narrays[1],
                                nan_policy='omit', **kwargs)

    xp_assert_close(res.statistic.data, xp.asarray(ref.statistic))
    xp_assert_close(res.pvalue.data, xp.asarray(ref.pvalue))

