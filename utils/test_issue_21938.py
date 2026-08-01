
def test_issue_21938():
    expr = sin(1/x + exp(-x)) - sin(1/x)
    assert expr.series(x, oo) == (1/(24*x**4) - 1/(2*x**2) + 1 + O(x**(-6), (x, oo)))*exp(-x)

