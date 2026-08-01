
def test_issue_14074():
    i = integrate(log(sin(x)), (x, 0, pi/2))
    assert not i.has(Integral)

