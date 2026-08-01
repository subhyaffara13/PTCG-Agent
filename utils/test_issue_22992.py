
def test_issue_22992():
    if not numpy:
        skip("numpy not installed")

    a, t = symbols('a t')
    expr = a*(log(cot(t/2)) - cos(t))
    F = lambdify([a, t], expr, 'numpy')

    point = {a: 10, t: 2}

    assert abs(expr.subs(point) - F(*point.values())) <= 1e-10

    # Standard math
    F = lambdify([a, t], expr)

    assert abs(expr.subs(point) - F(*point.values())) <= 1e-10

