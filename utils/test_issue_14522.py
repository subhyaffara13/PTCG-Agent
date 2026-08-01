
def test_issue_14522():
    eq = Poly(x**4 + x**3*(16 + 32*I) + x**2*(-285 + 386*I) + x*(-2824 - 448*I) - 2058 - 6053*I, x)
    roots_eq = roots(eq)
    assert all(eq(r) == 0 for r in roots_eq)

