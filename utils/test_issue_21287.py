
def test_issue_21287():
    assert not any(isinstance(i, Piecewise) for i in roots_quartic(
        Poly(x**4 - x**2*(3 + 5*I) + 2*x*(-1 + I) - 1 + 3*I, x)))

