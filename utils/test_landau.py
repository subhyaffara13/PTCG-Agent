
def test_landau():
    # Test that Landau distribution ufuncs are wrapped as expected;
    # accuracy is tested by Boost.
    x = np.linspace(-3, 10, 10)
    args = (0, 1)
    res = tanhsinh(lambda x: scu._landau_pdf(x, *args), -np.inf, x)
    cdf = scu._landau_cdf(x, *args)
    assert_allclose(res.integral, cdf)
    sf = scu._landau_sf(x, *args)
    assert_allclose(sf, 1-cdf)
    ppf = scu._landau_ppf(cdf, *args)
    assert_allclose(ppf, x)
    isf = scu._landau_isf(sf, *args)
    assert_allclose(isf, x, rtol=1e-6)

