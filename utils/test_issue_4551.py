
def test_issue_4551():
    assert not integrate(1/(x*sqrt(1 - x**2)), x).has(Integral)

