
def test_marcumq():
    m = Symbol('m')
    a = Symbol('a')
    b = Symbol('b')

    assert marcumq(0, 0, 0) == 0
    assert marcumq(m, 0, b) == uppergamma(m, b**2/2)/gamma(m)
    assert marcumq(2, 0, 5) == 27*exp(Rational(-25, 2))/2
    assert marcumq(0, a, 0) == 1 - exp(-a**2/2)
    assert marcumq(0, pi, 0) == 1 - exp(-pi**2/2)
    assert marcumq(1, a, a) == S.Half + exp(-a**2)*besseli(0, a**2)/2
    assert marcumq(2, a, a) == S.Half + exp(-a**2)*besseli(0, a**2)/2 + exp(-a**2)*besseli(1, a**2)

    assert diff(marcumq(1, a, 3), a) == a*(-marcumq(1, a, 3) + marcumq(2, a, 3))
    assert diff(marcumq(2, 3, b), b) == -b**2*exp(-b**2/2 - Rational(9, 2))*besseli(1, 3*b)/3

    x = Symbol('x')
    assert marcumq(2, 3, 4).rewrite(Integral, x=x) == \
           Integral(x**2*exp(-x**2/2 - Rational(9, 2))*besseli(1, 3*x), (x, 4, oo))/3
    assert eq([marcumq(5, -2, 3).rewrite(Integral).evalf(10)],
              [0.7905769565])

    k = Symbol('k')
    assert marcumq(-3, -5, -7).rewrite(Sum, k=k) == \
           exp(-37)*Sum((Rational(5, 7))**k*besseli(k, 35), (k, 4, oo))
    assert eq([marcumq(1, 3, 1).rewrite(Sum).evalf(10)],
              [0.9891705502])

    assert marcumq(1, a, a, evaluate=False).rewrite(besseli) == S.Half + exp(-a**2)*besseli(0, a**2)/2
    assert marcumq(2, a, a, evaluate=False).rewrite(besseli) == S.Half + exp(-a**2)*besseli(0, a**2)/2 + \
           exp(-a**2)*besseli(1, a**2)
    assert marcumq(3, a, a).rewrite(besseli) == (besseli(1, a**2) + besseli(2, a**2))*exp(-a**2) + \
           S.Half + exp(-a**2)*besseli(0, a**2)/2
    assert marcumq(5, 8, 8).rewrite(besseli) == exp(-64)*besseli(0, 64)/2 + \
           (besseli(4, 64) + besseli(3, 64) + besseli(2, 64) + besseli(1, 64))*exp(-64) + S.Half
    assert marcumq(m, a, a).rewrite(besseli) == marcumq(m, a, a)

    x = Symbol('x', integer=True)
    assert marcumq(x, a, a).rewrite(besseli) == marcumq(x, a, a)

