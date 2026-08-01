
def test_issue_12081():
    f = x**(Rational(-3, 2))*exp(-x)
    assert integrate(f, [x, 0, oo]) is oo

