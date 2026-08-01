
def test_issue_21594():
    assert simplify(exp(Rational(1,2)) + exp(Rational(-1,2))) == cosh(S.Half)*2

