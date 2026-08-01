
def test_issue_15471():
    f = log(x)*cos(log(x))/x**Rational(3, 4)
    F = -128*x**Rational(1, 4)*sin(log(x))/289 + 240*x**Rational(1, 4)*cos(log(x))/289 + (16*x**Rational(1, 4)*sin(log(x))/17 + 4*x**Rational(1, 4)*cos(log(x))/17)*log(x)
    assert_is_integral_of(f, F)

