
def test_issue_21860():
    e = 3*2**Rational(66666666667,200000000000)*3**Rational(16666666667,50000000000)*x**Rational(66666666667, 200000000000)
    ans = Mul(Rational(3, 2),
              Pow(Integer(2), Rational(33333333333, 100000000000)),
              Pow(Integer(3), Rational(26666666667, 40000000000)))
    assert e.xreplace({x: Rational(3,8)}) == ans

