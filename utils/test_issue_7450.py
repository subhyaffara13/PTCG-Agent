
def test_issue_7450():
    ans = integrate(exp(-(1 + I)*x), (x, 0, oo))
    assert re(ans) == S.Half and im(ans) == Rational(-1, 2)

