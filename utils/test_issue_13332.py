
def test_issue_13332():
    assert limit(sqrt(30)*5**(-5*x - 1)*(46656*x)**x*(5*x + 2)**(5*x + 5*S.Half) *
                (6*x + 2)**(-6*x - 5*S.Half), x, oo) == Rational(25, 36)

