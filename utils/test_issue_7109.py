
def test_issue_7109():
    assert not integrate(sqrt(a**2/(a**2 - x**2)), x).has(Integral)

