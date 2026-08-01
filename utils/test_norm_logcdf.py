
def test_norm_logcdf():
    # Test precision of the logcdf of the normal distribution.
    # This precision was enhanced in ticket 1614.
    x = -np.asarray(list(range(0, 120, 4)))
    # Values from R
    expected = [-0.69314718, -10.36010149, -35.01343716, -75.41067300,
                -131.69539607, -203.91715537, -292.09872100, -396.25241451,
                -516.38564863, -652.50322759, -804.60844201, -972.70364403,
                -1156.79057310, -1356.87055173, -1572.94460885, -1805.01356068,
                -2053.07806561, -2317.13866238, -2597.19579746, -2893.24984493,
                -3205.30112136, -3533.34989701, -3877.39640444, -4237.44084522,
                -4613.48339520, -5005.52420869, -5413.56342187, -5837.60115548,
                -6277.63751711, -6733.67260303]

    assert_allclose(stats.norm().logcdf(x), expected, atol=1e-8)

    # also test the complex-valued code path
    assert_allclose(stats.norm().logcdf(x + 1e-14j).real, expected, atol=1e-8)

    # test the accuracy: d(logcdf)/dx = pdf / cdf \equiv exp(logpdf - logcdf)
    deriv = (stats.norm.logcdf(x + 1e-10j)/1e-10).imag
    deriv_expected = np.exp(stats.norm.logpdf(x) - stats.norm.logcdf(x))
    assert_allclose(deriv, deriv_expected, atol=1e-10)

