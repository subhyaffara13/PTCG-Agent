
def test_issue_15810():
    assert integrate(1/(2**(2*x/3) + 1), (x, 0, oo)) == Rational(3, 2)

