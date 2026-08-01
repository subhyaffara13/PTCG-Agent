
def test_issue_4194():
    # simplify should call cancel
    f = Function('f')
    assert simplify((4*x + 6*f(y))/(2*x + 3*f(y))) == 2

