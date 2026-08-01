
def test_issue_6252():
    expr = 1/x/(a + b*x)**Rational(1, 3)
    anti = integrate(expr, x, meijerg=True)
    assert not anti.has(hyper)

