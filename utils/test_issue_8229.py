
def test_issue_8229():
    assert limit((x**Rational(1, 4) - 2)/(sqrt(x) - 4)**Rational(2, 3), x, 16) == 0

