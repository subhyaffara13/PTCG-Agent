
def check_moment_funcs(dist, result_shape):
    # Check that all computation methods of all distribution functions agree
    # with one another, effectively testing the correctness of the generic
    # computation methods and confirming the consistency of specific
    # distributions with their pdf/logpdf.

    atol = 1e-9  # make this tighter (e.g. 1e-13) after fixing `draw`

    def check(order, kind, method=None, ref=None, success=True):
        if success:
            res = dist.moment(order, kind, method=method)
            assert_allclose(res, ref, atol=atol*10**order)
            assert res.shape == ref.shape
        else:
            with pytest.raises(NotImplementedError):
                dist.moment(order, kind, method=method)

    def has_formula(order, kind):
        formula_name = f'_moment_{kind}_formula'
        overrides = dist._overrides(formula_name)
        if not overrides:
            return False
        formula = getattr(dist, formula_name)
        orders = getattr(formula, 'orders', set(range(6)))
        return order in orders

    dist.reset_cache()

    ### Check Raw Moments ###
    for i in range(6):
        check(i, 'raw', 'cache', success=False)  # not cached yet
        ref = dist.moment(i, 'raw', method='quadrature')
        check_nans_and_edges(dist, 'moment', None, ref)
        assert ref.shape == result_shape
        check(i, 'raw','cache', ref, success=True)  # cached now
        check(i, 'raw', 'formula', ref, success=has_formula(i, 'raw'))
        check(i, 'raw', 'general', ref, success=(i == 0))
        if dist.__class__ == stats.Normal:
            check(i, 'raw', 'quadrature_icdf', ref, success=True)


    # Clearing caches to better check their behavior
    dist.reset_cache()

    # If we have central or standard moment formulas, or if there are
    # values in their cache, we can use method='transform'
    dist.moment(0, 'central')  # build up the cache
    dist.moment(1, 'central')
    for i in range(2, 6):
        ref = dist.moment(i, 'raw', method='quadrature')
        check(i, 'raw', 'transform', ref,
              success=has_formula(i, 'central') or has_formula(i, 'standardized'))
        dist.moment(i, 'central')  # build up the cache
        check(i, 'raw', 'transform', ref)

    dist.reset_cache()

    ### Check Central Moments ###

    for i in range(6):
        check(i, 'central', 'cache', success=False)
        ref = dist.moment(i, 'central', method='quadrature')
        assert ref.shape == result_shape
        check(i, 'central', 'cache', ref, success=True)
        check(i, 'central', 'formula', ref, success=has_formula(i, 'central'))
        check(i, 'central', 'general', ref, success=i <= 1)
        if dist.__class__ == stats.Normal:
            check(i, 'central', 'quadrature_icdf', ref, success=True)
        if not (dist.__class__ == stats.Uniform and i == 5):
            # Quadrature is not super accurate for 5th central moment when the
            # support is really big. Skip this one failing test. We need to come
            # up with a better system of skipping individual failures w/ hypothesis.
            check(i, 'central', 'transform', ref,
                  success=has_formula(i, 'raw') or (i <= 1))
        if not has_formula(i, 'raw'):
            dist.moment(i, 'raw')
            check(i, 'central', 'transform', ref)

    variance = dist.variance()
    dist.reset_cache()

    # If we have standard moment formulas, or if there are
    # values in their cache, we can use method='normalize'
    dist.moment(0, 'standardized')  # build up the cache
    dist.moment(1, 'standardized')
    dist.moment(2, 'standardized')
    for i in range(3, 6):
        ref = dist.moment(i, 'central', method='quadrature')
        check(i, 'central', 'normalize', ref,
              success=has_formula(i, 'standardized') and not np.any(variance == 0))
        dist.moment(i, 'standardized')  # build up the cache
        check(i, 'central', 'normalize', ref, success=not np.any(variance == 0))

    ### Check Standardized Moments ###

    var = dist.moment(2, 'central', method='quadrature')
    dist.reset_cache()

    for i in range(6):
        check(i, 'standardized', 'cache', success=False)
        ref = dist.moment(i, 'central', method='quadrature') / var ** (i / 2)
        assert ref.shape == result_shape
        check(i, 'standardized', 'formula', ref,
              success=has_formula(i, 'standardized'))
        check(i, 'standardized', 'general', ref, success=i <= 2)
        check(i, 'standardized', 'normalize', ref)

    dist.reset_cache()

