
def test_keepdims(hypotest, args, kwds, n_samples, n_outputs, paired, unpacker,
                  sample_shape, axis_cases, nan_policy):
    small_sample_raises = {stats.skewtest, stats.kurtosistest, stats.normaltest,
                           stats.differential_entropy, stats.epps_singleton_2samp,
                           stats.shapiro}
    if sample_shape == (2, 3, 3, 4) and hypotest in small_sample_raises:
        pytest.skip("Sample too small; test raises error.")
    if hypotest in {weightedtau_weighted}:
        pytest.skip("`rankdata` used in testing doesn't support axis tuple.")
    # test if keepdims parameter works correctly
    if not unpacker:
        def unpacker(res):
            return res
    rng = np.random.default_rng(0)
    data = [rng.random(sample_shape) for _ in range(n_samples)]
    nan_data = [sample.copy() for sample in data]
    nan_mask = [rng.random(sample_shape) < 0.2 for _ in range(n_samples)]
    for sample, mask in zip(nan_data, nan_mask):
        sample[mask] = np.nan
    for axis in axis_cases:
        expected_shape = list(sample_shape)
        if axis is None:
            expected_shape = np.ones(len(sample_shape))
        else:
            if isinstance(axis, int):
                expected_shape[axis] = 1
            else:
                for ax in axis:
                    expected_shape[ax] = 1
        expected_shape = tuple(expected_shape)
        res = unpacker(hypotest(*data, *args, axis=axis, keepdims=True,
                                **kwds))
        res_base = unpacker(hypotest(*data, *args, axis=axis, keepdims=False,
                                     **kwds))
        nan_res = unpacker(hypotest(*nan_data, *args, axis=axis,
                                    keepdims=True, nan_policy=nan_policy,
                                    **kwds))
        nan_res_base = unpacker(hypotest(*nan_data, *args, axis=axis,
                                         keepdims=False,
                                         nan_policy=nan_policy, **kwds))
        for r, r_base, rn, rn_base in zip(res, res_base, nan_res,
                                          nan_res_base):
            assert r.shape == expected_shape
            r = np.squeeze(r, axis=axis)
            assert_allclose(r, r_base, atol=1e-16)
            assert rn.shape == expected_shape
            rn = np.squeeze(rn, axis=axis)
            # ideally assert_equal, but `combine_pvalues` failed on 32-bit build
            assert_allclose(rn, rn_base, atol=1e-16)

