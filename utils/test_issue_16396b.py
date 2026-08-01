
def test_issue_16396b():
    i = integrate(x*sin(x)/(1+cos(x)**2), (x, 0, pi))
    assert not i.has(Integral)

