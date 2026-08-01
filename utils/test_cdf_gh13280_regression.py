
def test_cdf_gh13280_regression(distname, args):
    # Test for nan output when shape parameters are invalid
    dist = getattr(stats, distname)
    x = np.arange(-2, 15)
    vals = dist.cdf(x, *args)
    expected = np.nan
    npt.assert_equal(vals, expected)

