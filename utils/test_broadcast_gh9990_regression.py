
def test_broadcast_gh9990_regression():
    # Regression test for gh-9990
    # The x-value 7 only lies within the support of 4 of the supplied
    # distributions.  Prior to 9990, one array passed to
    # stats.reciprocal._cdf would have 4 elements, but an array
    # previously stored by stats.reciprocal_argcheck() would have 6, leading
    # to a broadcast error.
    a = np.array([1, 2, 3, 4, 5, 6])
    b = np.array([8, 16, 1, 32, 1, 48])
    ans = [stats.reciprocal.cdf(7, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(7, a, b), ans)

    ans = [stats.reciprocal.cdf(1, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(1, a, b), ans)

    ans = [stats.reciprocal.cdf(_a, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(a, a, b), ans)

    ans = [stats.reciprocal.cdf(_b, _a, _b) for _a, _b in zip(a,b)]
    npt.assert_array_almost_equal(stats.reciprocal.cdf(b, a, b), ans)

