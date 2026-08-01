
def test_gh_pr_4806():
    # Check starting values for Cauchy distribution fit.
    rng = np.random.RandomState(1234)
    x = rng.randn(42)
    for offset in 10000.0, 1222333444.0:
        loc, scale = stats.cauchy.fit(x + offset)
        assert_allclose(loc, offset, atol=1.0)
        assert_allclose(scale, 0.6, atol=1.0)

