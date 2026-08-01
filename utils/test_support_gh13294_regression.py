
def test_support_gh13294_regression(distname, args):
    if distname in skip_test_support_gh13294_regression:
        pytest.skip(f"skipping test for the support method for "
                    f"distribution {distname}.")
    dist = getattr(stats, distname)
    # test support method with invalid arguments
    if isinstance(dist, stats.rv_continuous):
        # test with valid scale
        if len(args) != 0:
            a0, b0 = dist.support(*args)
            assert_equal(a0, np.nan)
            assert_equal(b0, np.nan)
        # test with invalid scale
        # For some distributions, that take no parameters,
        # the case of only invalid scale occurs and hence,
        # it is implicitly tested in this test case.
        loc1, scale1 = 0, -1
        a1, b1 = dist.support(*args, loc1, scale1)
        assert_equal(a1, np.nan)
        assert_equal(b1, np.nan)
    else:
        a, b = dist.support(*args)
        assert_equal(a, np.nan)
        assert_equal(b, np.nan)

