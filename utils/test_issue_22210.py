
def test_issue_22210():
    d = Symbol('d', integer=True)
    expr = 2*Derivative(sin(x), (x, d))
    assert expr.simplify() == expr

