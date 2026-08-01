
def test_issue_11877():
    x = symbols('x')
    assert integrate(log(S.Half - x), (x, 0, S.Half)) == Rational(-1, 2) -log(2)/2

