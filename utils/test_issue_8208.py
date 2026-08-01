
def test_issue_8208():
    assert limit(n**(Rational(1, 1e9) - 1), n, oo) == 0

