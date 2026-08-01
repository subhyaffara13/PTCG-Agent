
def test_issue_6828():
    f = 1/(1.08*x**2 - 4.3)
    g = integrate(f, x).diff(x)
    assert verify_numerically(f, g, tol=1e-12)

