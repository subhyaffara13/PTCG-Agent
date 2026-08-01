
def test_fewer_points_than_dimensions_gh17436():
    # When the number of points is fewer than the number of dimensions, the
    # the covariance matrix would be singular, and the exception tested in
    # test_singular_data_covariance_gh10205 would occur. However, sometimes
    # this occurs when the user passes in the transpose of what `gaussian_kde`
    # expects. This can result in a huge covariance matrix, so bail early.
    rng = np.random.default_rng(2046127537594925772)
    rvs = rng.multivariate_normal(np.zeros(3), np.eye(3), size=5)
    message = "Number of dimensions is greater than number of samples..."
    with pytest.raises(ValueError, match=message):
        stats.gaussian_kde(rvs)

