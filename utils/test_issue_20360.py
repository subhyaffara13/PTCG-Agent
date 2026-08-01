
def test_issue_20360():
    t, tau = symbols("t tau", real=True)
    n = symbols("n", integer=True)
    lam = pi * (n - S.Half)
    eq = integrate(exp(lam * tau), (tau, 0, t))
    assert eq.simplify() == (2*exp(pi*t*(2*n - 1)/2) - 2)/(pi*(2*n - 1))

