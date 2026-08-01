
def test_issue_11672():
    assert limit_seq(Rational(-1, 2)**n, n) == 0

