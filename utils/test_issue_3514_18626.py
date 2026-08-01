
def test_issue_3514_18626():
    assert sqrt(S.Half) * sqrt(6) == 2 * sqrt(3)/2
    assert S.Half*sqrt(6)*sqrt(2) == sqrt(3)
    assert sqrt(6)/2*sqrt(2) == sqrt(3)
    assert sqrt(6)*sqrt(2)/2 == sqrt(3)
    assert sqrt(8)**Rational(2, 3) == 2

