
def test_issue_7147():
    assert not integrate(x/sqrt(a*x**2 + b*x + c)**3, x).has(Integral)

