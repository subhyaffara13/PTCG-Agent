
def test_tukeylambda_stats_known_exact():
    """Compare results with some known exact formulas."""
    # Some exact values of the Tukey Lambda variance and kurtosis:
    # lambda   var      kurtosis
    #   0     pi**2/3     6/5     (logistic distribution)
    #  0.5    4 - pi    (5/3 - pi/2)/(pi/4 - 1)**2 - 3
    #   1      1/3       -6/5     (uniform distribution on (-1,1))
    #   2      1/12      -6/5     (uniform distribution on (-1/2, 1/2))

    # lambda = 0
    var = tukeylambda_variance(0)
    assert_allclose(var, np.pi**2 / 3, atol=1e-12)
    kurt = tukeylambda_kurtosis(0)
    assert_allclose(kurt, 1.2, atol=1e-10)

    # lambda = 0.5
    var = tukeylambda_variance(0.5)
    assert_allclose(var, 4 - np.pi, atol=1e-12)
    kurt = tukeylambda_kurtosis(0.5)
    desired = (5./3 - np.pi/2) / (np.pi/4 - 1)**2 - 3
    assert_allclose(kurt, desired, atol=1e-10)

    # lambda = 1
    var = tukeylambda_variance(1)
    assert_allclose(var, 1.0 / 3, atol=1e-12)
    kurt = tukeylambda_kurtosis(1)
    assert_allclose(kurt, -1.2, atol=1e-10)

    # lambda = 2
    var = tukeylambda_variance(2)
    assert_allclose(var, 1.0 / 12, atol=1e-12)
    kurt = tukeylambda_kurtosis(2)
    assert_allclose(kurt, -1.2, atol=1e-10)

