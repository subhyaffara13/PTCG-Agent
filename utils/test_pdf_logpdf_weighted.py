
def test_pdf_logpdf_weighted():
    rng = np.random.default_rng(1)
    n_basesample = 50
    xn = rng.normal(0, 1, n_basesample)
    wn = rng.random(n_basesample)

    # Default
    gkde = stats.gaussian_kde(xn, weights=wn)

    xs = np.linspace(-15, 12, 25)
    pdf = gkde.evaluate(xs)
    pdf2 = gkde.pdf(xs)
    assert_almost_equal(pdf, pdf2, decimal=12)

    logpdf = np.log(pdf)
    logpdf2 = gkde.logpdf(xs)
    assert_almost_equal(logpdf, logpdf2, decimal=12)

    # There are more points than data
    rng = np.random.default_rng(4531935345)
    gkde = stats.gaussian_kde(xs, weights=rng.random(len(xs)))
    pdf = np.log(gkde.evaluate(xn))
    pdf2 = gkde.logpdf(xn)
    assert_almost_equal(pdf, pdf2, decimal=12)

