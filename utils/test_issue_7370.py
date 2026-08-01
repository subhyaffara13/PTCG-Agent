
def test_issue_7370():
    f = Piecewise((1, x <= 2400))
    v = integrate(f, (x, 0, Float("252.4", 30)))
    assert str(v) == '252.400000000000000000000000000'

