
def test_kde_1d():
    #some basic tests comparing to normal distribution
    rng = np.random.default_rng(8765678)
    n_basesample = 500
    xn = rng.normal(0, 1, n_basesample)
    xnmean = xn.mean()
    xnstd = xn.std(ddof=1)

    # get kde for original sample
    gkde = stats.gaussian_kde(xn)

    # evaluate the density function for the kde for some points
    xx = np.asarray([0.1, 0.5, 0.9])
    loc, scale = gkde.dataset, np.sqrt(gkde.covariance)
    assert_allclose(
        gkde(xx), 
        stats.norm.pdf(xx[:, None], loc=loc, scale=scale).sum(axis=-1) / gkde.n,
        rtol=5e-14
    )

    xs = np.linspace(-7, 7, 501)
    kdepdf = gkde.evaluate(xs)
    normpdf = stats.norm.pdf(xs, loc=xnmean, scale=xnstd)
    intervall = xs[1] - xs[0]

    assert_(np.sum((kdepdf - normpdf)**2)*intervall < 0.01)
    prob1 = gkde.integrate_box_1d(xnmean, np.inf)
    prob2 = gkde.integrate_box_1d(-np.inf, xnmean)
    assert_almost_equal(prob1, 0.5, decimal=1)
    assert_almost_equal(prob2, 0.5, decimal=1)
    assert_almost_equal(gkde.integrate_box(xnmean, np.inf), prob1, decimal=13)
    assert_almost_equal(gkde.integrate_box(-np.inf, xnmean), prob2, decimal=13)

    assert_almost_equal(gkde.integrate_kde(gkde),
                        (kdepdf**2).sum()*intervall, decimal=2)
    assert_almost_equal(gkde.integrate_gaussian(xnmean, xnstd**2),
                        (kdepdf*normpdf).sum()*intervall, decimal=2)

