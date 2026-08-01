
def test_issue_15669():
    x = Symbol("x", positive=True)
    expr = (16*x**3/(-x**2 + sqrt(8*x**2 + (x**2 - 2)**2) + 2)**2 -
        2*2**Rational(4, 5)*x*(-x**2 + sqrt(8*x**2 + (x**2 - 2)**2) + 2)**Rational(3, 5) + 10*x)
    assert factor(expr, deep=True) == x*(x**2 + 2)

