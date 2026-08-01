
def test_minpoly_issue_7574():
    ex = -(-1)**Rational(1, 3) + (-1)**Rational(2,3)
    assert minimal_polynomial(ex, x) == x + 1

