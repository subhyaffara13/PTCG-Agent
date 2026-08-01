
def test_issue_7224():
    expr = sqrt(x)*besseli(1,sqrt(8*x))
    assert limit(x*diff(expr, x, x)/expr, x, 0) == 2
    assert limit(x*diff(expr, x, x)/expr, x, 1).evalf() == 2.0

