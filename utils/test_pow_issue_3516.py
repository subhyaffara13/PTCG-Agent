
def test_pow_issue_3516():
    assert 4**Rational(1, 4) == sqrt(2)

