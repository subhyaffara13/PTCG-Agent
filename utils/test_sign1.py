
def test_sign1():
    assert sign(Rational(0), x) == 0
    assert sign(Rational(3), x) == 1
    assert sign(Rational(-5), x) == -1
    assert sign(log(x), x) == 1
    assert sign(exp(-x), x) == 1
    assert sign(exp(x), x) == 1
    assert sign(-exp(x), x) == -1
    assert sign(3 - 1/x, x) == 1
    assert sign(-3 - 1/x, x) == -1
    assert sign(sin(1/x), x) == 1
    assert sign((x**Integer(2)), x) == 1
    assert sign(x**2, x) == 1
    assert sign(x**5, x) == 1

