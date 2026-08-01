
def test_issue_15076():
    sol = roots_quartic(Poly(t**4 - 6*t**2 + t/x - 3, t))
    assert sol[0].has(x)

