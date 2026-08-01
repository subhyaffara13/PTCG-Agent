
def test_issue_3692():
    assert ((-1)**Rational(1, 6)).expand(complex=True) == I/2 + sqrt(3)/2
    assert ((-5)**Rational(1, 6)).expand(complex=True) == \
        5**Rational(1, 6)*I/2 + 5**Rational(1, 6)*sqrt(3)/2
    assert ((-64)**Rational(1, 6)).expand(complex=True) == I + sqrt(3)

