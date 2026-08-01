
def test_gh9254_flag_if_maxiter_exceeded(maximum_iterations, flag_expected):
    """
    Test that if the maximum iterations is exceeded that the flag is not
    converged.
    """
    result = zeros.brentq(
        lambda x: ((1.2*x - 2.3)*x + 3.4)*x - 4.5,
        -30, 30, (), 1e-6, 1e-6, maximum_iterations,
        full_output=True, disp=False)
    assert result[1].flag == flag_expected
    if flag_expected == zeros.CONVERR:
        # didn't converge because exceeded maximum iterations
        assert result[1].iterations == maximum_iterations
    elif flag_expected == zeros.CONVERGED:
        # converged before maximum iterations
        assert result[1].iterations < maximum_iterations

