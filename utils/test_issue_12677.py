
def test_issue_12677():
    assert integrate(sin(x) / (cos(x)**3), (x, 0, pi/6)) == Rational(1, 6)

