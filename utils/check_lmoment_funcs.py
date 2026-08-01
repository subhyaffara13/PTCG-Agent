
def check_lmoment_funcs(dist, result_shape):
    # Perform consistency check for L-moments similar to check_moment_funcs above

    if not isinstance(dist, ContinuousDistribution):
        message = "L-moments are currently available only for continuous..."
        with pytest.raises(NotImplementedError, match=message):
            dist.lmoment(1)
        return

    atol = 2e-9

    def check(order, standardize=False, method=None, ref=None, success=True):
        if success:
            res = dist.lmoment(order, standardize=standardize, method=method)
            assert_allclose(res, ref, atol=atol)
            assert res.shape == ref.shape
        else:
            with pytest.raises(NotImplementedError):
                dist.lmoment(order, standardize=standardize, method=method)

    ### Check L-Moments ###

    standardize = False
    for i in range(1, 6):
        check(i, standardize, 'cache', success=standardize)  # not cached yet
        ref = dist.lmoment(i, standardize=standardize, method='order_statistics')
        check_nans_and_edges(dist, 'lmoment', None, ref)
        assert ref.shape == result_shape
        check(i, standardize, 'cache', ref, success=True)  # cached now
        check(i, standardize, 'formula', ref,
              success=dist._overrides('_lmoment_formula')
                      and (i < 5 or dist.__class__.__name__ == "Uniform"))
        check(i, standardize, 'general', ref, success=(i == 1))
        if dist._overrides('_icdf_formula'):
            check(i, standardize, 'quadrature_icdf', ref, success=True)

    standardize=True
    for i in range(3, 6):
        ref = dist.lmoment(i, standardize=standardize, method='order_statistics')
        assert ref.shape == result_shape
        check(i, standardize, 'formula', ref,
              success=dist._overrides('_lmoment_formula')
                      and (i < 5 or dist.__class__.__name__ == "Uniform"))
        check(i, standardize, 'general', ref, success=False)
        if dist._overrides('_icdf_formula'):
            check(i, standardize, 'quadrature_icdf', ref, success=True)

