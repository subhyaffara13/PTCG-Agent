
def test_issue_21762():
    e = (x**2 + 6)**(Integer(33333333333333333)/50000000000000000)
    ans = Mul(Rational(5, 4),
              Pow(Integer(2), Rational(16666666666666667, 25000000000000000)),
              Pow(Integer(5), Rational(8333333333333333, 25000000000000000)))
    assert e.xreplace({x: S.Half}) == ans

