
def check_sample_shape_NaNs(dist, fname, sample_shape, result_shape, rng):
    full_shape = sample_shape + result_shape
    if fname == 'sample':
        sample_method = dist.sample

    methods = {'inverse_transform'}
    if dist._overrides(f'_{fname}_formula') and not isinstance(rng, qmc.QMCEngine):
        methods.add('formula')

    for method in methods:
        res = sample_method(sample_shape, method=method, rng=rng)
        valid_parameters = np.broadcast_to(get_valid_parameters(dist),
                                           res.shape)
        assert_equal(res.shape, full_shape)
        np.testing.assert_equal(res.dtype, dist._dtype)

        if full_shape == ():
            # NumPy random makes a distinction between a 0d array and a scalar.
            # In stats, we consistently turn 0d arrays into scalars, so
            # maintain that behavior here. (With Array API arrays, this will
            # change.)
            assert np.isscalar(res)
        assert np.all(np.isfinite(res[valid_parameters]))
        assert_equal(res[~valid_parameters], np.nan)

        sample1 = sample_method(sample_shape, method=method, rng=42)
        sample2 = sample_method(sample_shape, method=method, rng=42)
        if not isinstance(dist, DiscreteDistribution):
            # The idea is that it's very unlikely that the random sample
            # for a randomly chosen seed will match that for seed 42,
            # but it is not so unlikely if `dist` is a discrete distribution.
            assert not np.any(np.equal(res, sample1))
        assert_equal(sample1, sample2)

