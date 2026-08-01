
def test_issue_11813():
    assert not integrate((a - x)**Rational(-1, 2)*x, (x, 0, a)).has(Integral)

