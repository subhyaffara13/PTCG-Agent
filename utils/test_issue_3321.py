
def test_issue_3321():
    assert sqrt(Rational(1, 5)) == Rational(1, 5)**S.Half
    assert 5 * sqrt(Rational(1, 5)) == sqrt(5)

