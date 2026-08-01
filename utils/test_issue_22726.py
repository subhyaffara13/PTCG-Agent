
def test_issue_22726():
    if not numpy:
        skip("numpy not installed")

    x1, x2 = symbols('x1 x2')
    f = Max(S.Zero, Min(x1, x2))
    g = derive_by_array(f, (x1, x2))
    G = lambdify((x1, x2), g, modules='numpy')
    point = {x1: 1, x2: 2}
    assert (abs(g.subs(point) - G(*point.values())) <= 1e-10).all()

