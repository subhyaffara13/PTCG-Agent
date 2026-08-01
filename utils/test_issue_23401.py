
def test_issue_23401():
    x = Symbol('x')
    expr = (x + 1)/(-1.0e-3*x**2 + 0.1*x + 0.1)
    assert is_increasing(expr, Interval(1,2), x)

