
def test_issue_10584():
    assert not integrate(sqrt(x**2 + 1/x**2), x).has(Integral)

