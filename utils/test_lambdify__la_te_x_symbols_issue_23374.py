
def test_lambdify_LaTeX_symbols_issue_23374():
    # Create symbols with Latex style names
    x1, x2 = symbols("x_{1} x_2")

    # Lambdify the function
    f1 = lambdify([x1, x2], cos(x1 ** 2 + x2 ** 2))

    # Test that the function works correctly (numerically)
    assert f1(1, 2) == math_cos(1 ** 2 + 2 ** 2)

    # Explicitly generate a custom printer to verify the naming convention
    p = LambdaPrinter()
    expr_str = p.doprint(cos(x1 ** 2 + x2 ** 2))
    assert 'x_1' in expr_str
    assert 'x_2' in expr_str

