
def test_issue_15227():
    i = integrate(log(1-x)*log((1+x)**2)/x, (x, 0, 1))
    assert not i.has(Integral)

