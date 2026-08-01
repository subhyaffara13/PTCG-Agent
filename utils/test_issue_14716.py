
def test_issue_14716():
    i = integrate(log(x + 5)*cos(pi*x),(x, S.Half, 1))
    assert not i.has(Integral)

