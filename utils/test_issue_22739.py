
def test_issue_22739():
    if not numpy:
        skip("numpy not installed")

    x1, x2 = symbols('x1 x2')
    f = Heaviside(Min(x1, x2))
    F = lambdify((x1, x2), f, modules='numpy')
    point = {x1: 1, x2: 2}
    assert abs(f.subs(point) - F(*point.values())) <= 1e-10

