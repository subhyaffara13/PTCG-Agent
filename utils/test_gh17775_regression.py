
def test_gh17775_regression(x, n, sf, cdf, pdf, rtol):
    # Regression test for gh-17775. In scipy 1.9.3 and earlier,
    # these test would fail.
    #
    # KS one asymptotic sf ~ e^(-(6nx+1)^2 / 18n)
    # Given a large 32-bit integer n, 6n will overflow in the c implementation.
    # Example of broken behaviour:
    # ksone.sf(2.0e-5, 1000000000) == 0.9374359693473666
    ks = stats.ksone
    vals = np.array([ks.sf(x, n), ks.cdf(x, n), ks.pdf(x, n)])
    expected = np.array([sf, cdf, pdf])
    npt.assert_allclose(vals, expected, rtol=rtol)
    # The sf+cdf must sum to 1.0.
    npt.assert_equal(vals[0] + vals[1], 1.0)
    # Check inverting the (potentially very small) sf (uses a lower tolerance)
    npt.assert_allclose([ks.isf(sf, n)], [x], rtol=1e-8)

