
def test_issue_14709a():
    i = integrate(x*acos(1 - 2*x/h), (x, 0, h))
    assert not i.has(Integral)

