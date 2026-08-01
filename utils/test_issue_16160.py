
def test_issue_16160():
    assert Derivative(x**3, (x, x)).subs(x, 2) == Subs(
        Derivative(x**3, (x, 2)), x, 2)
    assert Derivative(1 + x**3, (x, x)).subs(x, 0
        ) == Derivative(1 + y**3, (y, 0)).subs(y, 0)

