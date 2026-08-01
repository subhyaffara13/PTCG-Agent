
def test_issue_4822():
    z = (-1)**Rational(1, 3)*(1 - I*sqrt(3))
    assert z.is_real in [True, None]

