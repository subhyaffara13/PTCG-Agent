
def test_simplify_issue_1308():
    assert simplify(exp(Rational(-1, 2)) + exp(Rational(-3, 2))) == \
        (1 + E)*exp(Rational(-3, 2))

