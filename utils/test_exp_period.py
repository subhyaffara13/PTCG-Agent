
def test_exp_period():
    assert exp(I*pi*Rational(9, 4)) == exp(I*pi/4)
    assert exp(I*pi*Rational(46, 18)) == exp(I*pi*Rational(5, 9))
    assert exp(I*pi*Rational(25, 7)) == exp(I*pi*Rational(-3, 7))
    assert exp(I*pi*Rational(-19, 3)) == exp(-I*pi/3)
    assert exp(I*pi*Rational(37, 8)) - exp(I*pi*Rational(-11, 8)) == 0
    assert exp(I*pi*Rational(-5, 3)) / exp(I*pi*Rational(11, 5)) * exp(I*pi*Rational(148, 15)) == 1

    assert exp(2 - I*pi*Rational(17, 5)) == exp(2 + I*pi*Rational(3, 5))
    assert exp(log(3) + I*pi*Rational(29, 9)) == 3 * exp(I*pi*Rational(-7, 9))

    n = Symbol('n', integer=True)
    e = Symbol('e', even=True)
    assert exp(e*I*pi) == 1
    assert exp((e + 1)*I*pi) == -1
    assert exp((1 + 4*n)*I*pi/2) == I
    assert exp((-1 + 4*n)*I*pi/2) == -I

