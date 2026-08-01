
def check_ccdf2(dist, log, x, y, result_shape, methods):
    # Specialized test for 2-arg ccdf since the interface is a bit different
    # from the other methods. Could be combined with check_cdf2 above, but
    # writing it separately is simpler.
    methods = methods.copy()

    if dist._overrides(f'_{"log" if log else ""}ccdf2_formula'):
        methods.add('formula')

    ref = dist.cdf(x) + dist.ccdf(y)
    np.testing.assert_equal(ref.shape, result_shape)

    if result_shape == tuple():
        assert np.isscalar(ref)

    for method in methods:
        message = ("Two argument cdf functions are currently only supported for "
                   "continuous distributions.")
        if isinstance(dist, DiscreteDistribution):
            with pytest.raises(NotImplementedError, match=message):
                res = (np.exp(dist.logccdf(x, y, method=method)) if log
                       else dist.ccdf(x, y, method=method))
            continue
        res = (np.exp(dist.logccdf(x, y, method=method)) if log
               else dist.ccdf(x, y, method=method))
        np.testing.assert_allclose(res, ref, atol=1e-14)
        np.testing.assert_equal(res.dtype, ref.dtype)
        np.testing.assert_equal(res.shape, result_shape)
        if result_shape == tuple():
            assert np.isscalar(res)

