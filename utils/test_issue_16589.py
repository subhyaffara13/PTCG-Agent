
def test_issue_16589():
    eq = Poly(x**4 - 8*sqrt(2)*x**3 + 4*x**3 - 64*sqrt(2)*x**2 + 1024*x, x)
    roots_eq = roots(eq)
    assert 0 in roots_eq

