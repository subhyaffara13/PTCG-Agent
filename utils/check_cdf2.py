
def check_cdf2(dist, log, x, y, result_shape, methods):
    # Specialized test for 2-arg cdf since the interface is a bit different
    # from the other methods. Here, we'll use 1-arg cdf as a reference, and
    # since we have already checked 1-arg cdf in `check_nans_and_edges`, this
    # checks the equivalent of both `check_dist_func` and
    # `check_nans_and_edges`.
    methods = methods.copy()

    if log:
        if dist._overrides('_logcdf2_formula'):
            methods.add('formula')
        if dist._overrides('_logcdf_formula') or dist._overrides('_logccdf_formula'):
            methods.add('subtraction')
        if (dist._overrides('_cdf_formula')
                or dist._overrides('_ccdf_formula')):
            methods.add('log/exp')
    else:
        if dist._overrides('_cdf2_formula'):
            methods.add('formula')
        if dist._overrides('_cdf_formula') or dist._overrides('_ccdf_formula'):
            methods.add('subtraction')
        if (dist._overrides('_logcdf_formula')
                or dist._overrides('_logccdf_formula')):
            methods.add('log/exp')

    ref = dist.cdf(y) - dist.cdf(x)
    np.testing.assert_equal(ref.shape, result_shape)

    if result_shape == tuple():
        assert np.isscalar(ref)

    for method in methods:
        if isinstance(dist, DiscreteDistribution):
            message = ("Two argument cdf functions are currently only supported for "
                       "continuous distributions.")
            with pytest.raises(NotImplementedError, match=message):
                res = (np.exp(dist.logcdf(x, y, method=method)) if log
                       else dist.cdf(x, y, method=method))
            continue
        res = (np.exp(dist.logcdf(x, y, method=method)) if log
               else dist.cdf(x, y, method=method))
        np.testing.assert_allclose(res, ref, atol=1e-14)
        if log:
            np.testing.assert_equal(res.dtype, (ref + 0j).dtype)
        else:
            np.testing.assert_equal(res.dtype, ref.dtype)
        np.testing.assert_equal(res.shape, result_shape)
        if result_shape == tuple():
            assert np.isscalar(res)

