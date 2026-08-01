
def test_definite_integral_with_floats_issue_27231():
    # Define the symbol and the integral expression
    x = symbols('x', real=True)
    integral_expr = sqrt(1 - 0.5625 * (x + 0.333333333333333) ** 2)

    # Perform the definite integral with the known limits
    result_symbolic = integrate(integral_expr, (x, -1, 1))
    result_numeric = result_symbolic.evalf()

    # Expected result with higher precision
    expected_result = sqrt(3) / 6 + 4 * pi / 9

    # Verify that the result is approximately equal within a larger tolerance
    assert abs(result_numeric - expected_result.evalf()) < 1e-8

