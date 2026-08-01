
def test_singular_data_covariance_gh10205():
    # When the data lie in a lower-dimensional subspace and this causes
    # and exception, check that the error message is informative.
    rng = np.random.default_rng(2321583144339784787)
    mu = np.array([1, 10, 20])
    sigma = np.array([[4, 10, 0], [10, 25, 0], [0, 0, 100]])
    data = rng.multivariate_normal(mu, sigma, 1000)
    try:  # doesn't raise any error on some platforms, and that's OK
        stats.gaussian_kde(data.T)
    except linalg.LinAlgError:
        msg = "The data appears to lie in a lower-dimensional subspace..."
        with assert_raises(linalg.LinAlgError, match=msg):
            stats.gaussian_kde(data.T)

