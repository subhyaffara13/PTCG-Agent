
def test_log_exp():
    assert log(exp(4*I*pi)) == 0     # exp evaluates
    assert log(exp(-5*I*pi)) == I*pi # exp evaluates
    assert log(exp(I*pi*Rational(19, 4))) == I*pi*Rational(3, 4)
    assert log(exp(I*pi*Rational(25, 7))) == I*pi*Rational(-3, 7)
    assert log(exp(-5*I)) == -5*I + 2*I*pi

