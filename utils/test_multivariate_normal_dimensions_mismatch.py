
def test_multivariate_normal_dimensions_mismatch():
    # Regression test for GH #3493. Check that setting up a PDF with a mean of
    # length M and a covariance matrix of size (N, N), where M != N, raises a
    # ValueError with an informative error message.
    mu = np.array([0.0, 0.0])
    sigma = np.array([[1.0]])

    assert_raises(ValueError, multivariate_normal, mu, sigma)

    # A simple check that the right error message was passed along. Checking
    # that the entire message is there, word for word, would be somewhat
    # fragile, so we just check for the leading part.
    try:
        multivariate_normal(mu, sigma)
    except ValueError as e:
        msg = "Dimension mismatch"
        assert_equal(str(e)[:len(msg)], msg)

