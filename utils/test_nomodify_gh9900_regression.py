
def test_nomodify_gh9900_regression():
    # Regression test for gh-9990
    # Prior to gh-9990, calls to stats.truncnorm._cdf() use what ever was
    # set inside the stats.truncnorm instance during stats.truncnorm.cdf().
    # This could cause issues with multi-threaded code.
    # Since then, the calls to cdf() are not permitted to modify the global
    # stats.truncnorm instance.
    tn = stats.truncnorm
    # Use the right-half truncated normal
    # Check that the cdf and _cdf return the same result.
    npt.assert_almost_equal(tn.cdf(1, 0, np.inf),
                            0.6826894921370859)
    npt.assert_almost_equal(tn._cdf([1], [0], [np.inf]),
                            0.6826894921370859)

    # Now use the left-half truncated normal
    npt.assert_almost_equal(tn.cdf(-1, -np.inf, 0),
                            0.31731050786291415)
    npt.assert_almost_equal(tn._cdf([-1], [-np.inf], [0]),
                            0.31731050786291415)

    # Check that the right-half truncated normal _cdf hasn't changed
    npt.assert_almost_equal(tn._cdf([1], [0], [np.inf]),
                            0.6826894921370859)  # Not 1.6826894921370859
    npt.assert_almost_equal(tn.cdf(1, 0, np.inf),
                            0.6826894921370859)

    # Check that the left-half truncated normal _cdf hasn't changed
    npt.assert_almost_equal(tn._cdf([-1], [-np.inf], [0]),
                            0.31731050786291415)  # Not -0.6826894921370859
    npt.assert_almost_equal(tn.cdf(1, -np.inf, 0),
                            1)  # Not 1.6826894921370859
    npt.assert_almost_equal(tn.cdf(-1, -np.inf, 0),
                            0.31731050786291415)  # Not -0.6826894921370859

