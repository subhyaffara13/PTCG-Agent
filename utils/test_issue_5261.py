
def test_issue_5261():
    x = symbols('x', real=True)
    e = I*x
    assert exp(e).subs(exp(x), y) == y**I
    assert (2**e).subs(2**x, y) == y**I
    eq = (-2)**e
    assert eq.subs((-2)**x, y) == eq

