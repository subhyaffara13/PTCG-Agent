
def test_kde_1d_weighted():
    #some basic tests comparing to normal distribution
    rng = np.random.default_rng(8765678)
    n_basesample = 500
    xn = rng.normal(0, 1, n_basesample)
    wn = rng.random(n_basesample)
    xnmean = np.average(xn, weights=wn)
    xnstd = np.sqrt(np.average((xn-xnmean)**2, weights=wn))

    # get kde for original sample
    gkde = stats.gaussian_kde(xn, weights=wn)

    # evaluate the density function for the kde for some points
    # evaluate the density function for the kde for some points
    xx = np.asarray([0.1, 0.5, 0.9])
    loc, scale = gkde.dataset, np.sqrt(gkde.covariance)

    pdf = stats.norm.pdf
    assert_allclose(
        gkde(xx), 
        np.sum(pdf(xx[:, None], loc=loc, scale=scale) * gkde.weights, axis=-1),
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

