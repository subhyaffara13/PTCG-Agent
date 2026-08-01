
def test_issue_4941():
    assert not integrate(sqrt(1 + sinh(x/20)**2), (x, -25, 25)).has(Integral)

