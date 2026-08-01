
def test_issue_6318():
    eq = (1/x)**Rational(2, 3)
    assert (eq + 1).as_leading_term(x) == eq

