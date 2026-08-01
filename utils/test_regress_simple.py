
def test_regress_simple():
    # Regress a line with sinusoidal noise. Test for #1273.
    x = np.linspace(0, 100, 100)
    y = 0.2 * np.linspace(0, 100, 100) + 10
    y += np.sin(np.linspace(0, 20, 100))

    result = mstats.linregress(x, y)

    # Result is of a correct class and with correct fields
    lr = _stats_py.LinregressResult
    assert_(isinstance(result, lr))
    attributes = ('slope', 'intercept', 'rvalue', 'pvalue', 'stderr')
    check_named_results(result, attributes, ma=True)
    assert 'intercept_stderr' in dir(result)

    # Slope and intercept are estimated correctly
    assert_almost_equal(result.slope, 0.19644990055858422)
    assert_almost_equal(result.intercept, 10.211269918932341)
    assert_almost_equal(result.stderr, 0.002395781449783862)
    assert_almost_equal(result.intercept_stderr, 0.13866936078570702)

