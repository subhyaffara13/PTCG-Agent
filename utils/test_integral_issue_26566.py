
def test_integral_issue_26566():
    # Define the symbols
    x = symbols('x', real=True)
    a = symbols('a', real=True, positive=True)

    # Define the integral expression
    integral_expr = sin(a * (x + pi))**2
    symbolic_result = integrate(integral_expr, (x, -pi, -pi/2))

    # Known correct result
    correct_result = pi / 4

    # Substitute a specific value for 'a' to evaluate both results
    a_value = 1
    numeric_symbolic_result = symbolic_result.subs(a, a_value).evalf()
    numeric_correct_result = correct_result.evalf()

    # Assert that the symbolic result matches the correct value
    assert simplify(numeric_symbolic_result - numeric_correct_result) == 0

