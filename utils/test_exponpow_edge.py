
def test_exponpow_edge():
    # Regression test for gh-3982.
    p = stats.exponpow.logpdf(0, 1)
    assert_equal(p, 0.0)

    # Check pdf and logpdf at x = 0 for other values of b.
    p = stats.exponpow.pdf(0, [0.25, 1.0, 1.5])
    assert_equal(p, [np.inf, 1.0, 0.0])
    p = stats.exponpow.logpdf(0, [0.25, 1.0, 1.5])
    assert_equal(p, [np.inf, 0.0, -np.inf])

