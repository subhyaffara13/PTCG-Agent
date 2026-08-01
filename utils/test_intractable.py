
def test_intractable():
    assert gruntz(1/gamma(x), x, oo) == 0
    assert gruntz(1/loggamma(x), x, oo) == 0
    assert gruntz(gamma(x)/loggamma(x), x, oo) is oo
    assert gruntz(exp(gamma(x))/gamma(x), x, oo) is oo
    assert gruntz(gamma(x), x, 3) == 2
    assert gruntz(gamma(Rational(1, 7) + 1/x), x, oo) == gamma(Rational(1, 7))
    assert gruntz(log(x**x)/log(gamma(x)), x, oo) == 1
    assert gruntz(log(gamma(gamma(x)))/exp(x), x, oo) is oo

