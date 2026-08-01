
def test_issue_16396a():
    i = integrate(1/(1+sqrt(tan(x))), (x, pi/3, pi/6))
    assert not i.has(Integral)

