
def test_kde_bandwidth_method():
    def scotts_factor(kde_obj):
        """Same as default, just check that it works."""
        return np.power(kde_obj.n, -1./(kde_obj.d+4))

    rng = np.random.default_rng(8765678)
    n_basesample = 50
    xn = rng.normal(0, 1, n_basesample)

    # Default
    gkde = stats.gaussian_kde(xn)
    # Supply a callable
    gkde2 = stats.gaussian_kde(xn, bw_method=scotts_factor)
    # Supply a scalar
    gkde3 = stats.gaussian_kde(xn, bw_method=gkde.factor)

    xs = np.linspace(-7,7,51)
    kdepdf = gkde.evaluate(xs)
    kdepdf2 = gkde2.evaluate(xs)
    assert_almost_equal(kdepdf, kdepdf2)
    kdepdf3 = gkde3.evaluate(xs)
    assert_almost_equal(kdepdf, kdepdf3)

    assert_raises(ValueError, stats.gaussian_kde, xn, bw_method='wrongstring')

