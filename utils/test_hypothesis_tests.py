
def test_hypothesis_tests(f_name, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        f = getattr(stats, f_name)

        n = 2 if f_name in {'ttest_1samp', 'ttest_rel', 'ttest_ind', 'bartlett',
                            'pearsonr', 'chisquare'} else 1

        arrays = get_arrays(n, xp=xp, dtype=dtype, device=device)
        if f_name == 'ttest_1samp':
            arrays[1] = xp.mean(arrays[1])
        if f_name == 'chisquare':
            arrays[1] = xp.sum(arrays[0]) * arrays[1] / xp.sum(arrays[1])

        res = f(*arrays)
        assert xp_device(res.statistic) == xp_device(arrays[0])
        assert xp_device(res.pvalue) == xp_device(arrays[0])
        assert res.statistic.dtype == dtype
        assert res.pvalue.dtype == dtype

        if f_name in {'ttest_1samp', 'ttest_rel', 'ttest_ind', 'pearsonr'}:
            res_ci = res.confidence_interval()
            assert xp_device(res_ci.low) == xp_device(arrays[0])
            assert xp_device(res_ci.high) == xp_device(arrays[0])
            assert res_ci.low.dtype == dtype
            assert res_ci.high.dtype == dtype

