
def test_issue_14398():
    assert not integrate(exp(x**2)*cos(x), x).has(Integral)

