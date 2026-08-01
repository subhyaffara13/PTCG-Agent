
def test_wrightomega_exp_approximation_crossover():
    desired_error = 2 * np.finfo(float).eps
    crossover = -50
    x_before_crossover = np.nextafter(crossover, np.inf)
    x_after_crossover = np.nextafter(crossover, -np.inf)
    # Computed using Mpmath
    desired_before_crossover = 1.9287498479639314876e-22
    desired_after_crossover = 1.9287498479639040784e-22
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

