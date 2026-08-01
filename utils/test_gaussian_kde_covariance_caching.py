
def test_gaussian_kde_covariance_caching():
    x1 = np.array([-7, -5, 1, 4, 5], dtype=float)
    xs = np.linspace(-10, 10, num=5)
    # These expected values are from scipy 0.10, before some changes to
    # gaussian_kde.  They were not compared with any external reference.
    y_expected = [0.02463386, 0.04689208, 0.05395444, 0.05337754, 0.01664475]

    # Set the bandwidth, then reset it to the default.
    kde = stats.gaussian_kde(x1)
    kde.set_bandwidth(bw_method=0.5)
    kde.set_bandwidth(bw_method='scott')
    y2 = kde(xs)

    assert_array_almost_equal(y_expected, y2, decimal=7)

