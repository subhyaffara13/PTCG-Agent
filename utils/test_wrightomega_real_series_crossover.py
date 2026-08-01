
def test_wrightomega_real_series_crossover():
    desired_error = 2 * np.finfo(float).eps
    crossover = 1e20
    x_before_crossover = np.nextafter(crossover, -np.inf)
    x_after_crossover = np.nextafter(crossover, np.inf)
    # Computed using Mpmath
    desired_before_crossover = 99999999999999983569.948
    desired_after_crossover = 100000000000000016337.948
    assert_allclose(
        sc.wrightomega(x_before_crossover),
        desired_before_crossover,
        atol=0,
        rtol=desired_error,
    )
    assert_allclose(
        sc.wrightomega(x_after_crossover),
        desired_after_crossover,
        atol=0,
        rtol=desired_error,
    )

