
def test_sf_isf_overrides(case):
    # Test that SF is the inverse of ISF. Supplements
    # `test_continuous_basic.check_sf_isf` for distributions with overridden
    # `sf` and `isf` methods.
    distname, lp1, lp2, atol, rtol = case

    lpm = np.log10(0.5)  # log10 of the probability mass at the median
    lp1 = lp1 or -290
    lp2 = lp2 or -14
    atol = atol or 0
    rtol = rtol or 1e-12
    dist = getattr(stats, distname)
    params = dict(distcont)[distname]
    dist_frozen = dist(*params)

    # Test (very deep) right tail to median. We can benchmark with random
    # (loguniform) points, but strictly logspaced points are fine for tests.
    ref = np.logspace(lp1, lpm)
    res = dist_frozen.sf(dist_frozen.isf(ref))
    assert_allclose(res, ref, atol=atol, rtol=rtol)

    # test median to left tail
    ref = 1 - np.logspace(lp2, lpm, 20)
    res = dist_frozen.sf(dist_frozen.isf(ref))
    assert_allclose(res, ref, atol=atol, rtol=rtol)

