
def test_issue_15226():
    assert Subs(Derivative(f(y), x, y), y, g(x)).doit() != 0

