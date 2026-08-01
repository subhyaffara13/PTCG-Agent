
def test_issue_14078b():
    i = integrate((atan(4*x)-atan(2*x))/x, (x, 0, oo))
    assert not i.has(Integral)

