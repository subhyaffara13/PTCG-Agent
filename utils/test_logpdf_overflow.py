
def test_logpdf_overflow():
    # regression test for gh-12988; testing against linalg instability for
    # very high dimensionality kde
    rng = np.random.default_rng(1)
    n_dimensions = 2500
    n_samples = 5000
    xn = np.array([rng.normal(0, 1, n_samples) + (n) for n in range(
        0, n_dimensions)])

    # Default
    gkde = stats.gaussian_kde(xn)

    logpdf = gkde.logpdf(np.arange(0, n_dimensions))
    np.testing.assert_equal(np.isneginf(logpdf[0]), False)
    np.testing.assert_equal(np.isnan(logpdf[0]), False)

