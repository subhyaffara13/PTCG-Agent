
def test_cos():
    e = cos(x).lseries(x)
    assert next(e) == 1
    assert next(e) == -x**2/2
    assert next(e) == x**4/24


def test_cos():
    e1 = cos(x).series(x, 0)
    e2 = series(cos(x), x, 0)
    assert e1 == e2


def test_cos():
    R, x, y = ring('x, y', QQ)
    assert rs_cos(x, x, 9) == 1 - x**2/2 + x**4/24 - x**6/720 + x**8/40320
    assert rs_cos(x*y + x**2*y**3, x, 9) == x**8*y**12/24 - \
        x**8*y**10/48 + x**8*y**8/40320 + x**7*y**10/6 - \
        x**7*y**8/120 + x**6*y**8/4 - x**6*y**6/720 + x**5*y**6/6 - \
        x**4*y**6/2 + x**4*y**4/24 - x**3*y**4 - x**2*y**2/2 + 1

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', QQ[sin(a), cos(a), a])
    assert rs_cos(x + a, x, 5) == cos(a)*x**4/24 + sin(a)*x**3/6 - \
        cos(a)*x**2/2 - sin(a)*x + cos(a)
    assert rs_cos(x + x**2*y + a, x, 5) == -cos(a)*x**4*y**2/2 + \
        sin(a)*x**4*y/2 + cos(a)*x**4/24 - cos(a)*x**3*y + sin(a)*x**3/6 - \
        sin(a)*x**2*y - cos(a)*x**2/2 - sin(a)*x + cos(a)

    R, x, y = ring('x, y', EX)
    assert rs_cos(x + a, x, 5) == EX(cos(a)/24)*x**4 + EX(sin(a)/6)*x**3 - \
        EX(cos(a)/2)*x**2 - EX(sin(a))*x + EX(cos(a))
    assert rs_cos(x + x**2*y + a, x, 5) == -EX(cos(a)/2)*x**4*y**2 + \
        EX(sin(a)/2)*x**4*y + EX(cos(a)/24)*x**4 - EX(cos(a))*x**3*y + \
        EX(sin(a)/6)*x**3 - EX(sin(a))*x**2*y - EX(cos(a)/2)*x**2 - \
        EX(sin(a))*x + EX(cos(a))


def test_cos():
    a = cos(interval(0, np.pi / 4))
    assert a.start == np.cos(np.pi / 4)
    assert a.end == 1

    a = cos(interval(-np.pi / 4, np.pi / 4))
    assert a.start == np.cos(-np.pi / 4)
    assert a.end == 1

    a = cos(interval(np.pi / 4, 3 * np.pi / 4))
    assert a.start == np.cos(3 * np.pi / 4)
    assert a.end == np.cos(np.pi / 4)

    a = cos(interval(3 * np.pi / 4, 5 * np.pi / 4))
    assert a.start == -1
    assert a.end == np.cos(3 * np.pi / 4)

    a = cos(interval(0, 3 * np.pi))
    assert a.start == -1
    assert a.end == 1

    a = cos(interval(- np.pi / 3, 5 * np.pi / 4))
    assert a.start == -1
    assert a.end == 1

    a = cos(interval(1, 2, is_valid=False))
    assert a.is_valid is False


def test_cos():
    x, y = symbols('x y')

    assert cos.nargs == FiniteSet(1)
    assert cos(nan) is nan

    assert cos(oo) == AccumBounds(-1, 1)
    assert cos(oo) - cos(oo) == AccumBounds(-2, 2)
    assert cos(oo*I) is oo
    assert cos(-oo*I) is oo
    assert cos(zoo) is nan

    assert cos(0) == 1

    assert cos(acos(x)) == x
    assert cos(atan(x)) == 1 / sqrt(1 + x**2)
    assert cos(asin(x)) == sqrt(1 - x**2)
    assert cos(acot(x)) == 1 / sqrt(1 + 1 / x**2)
    assert cos(acsc(x)) == sqrt(1 - 1 / x**2)
    assert cos(asec(x)) == 1 / x
    assert cos(atan2(y, x)) == x / sqrt(x**2 + y**2)

    assert cos(pi*I) == cosh(pi)
    assert cos(-pi*I) == cosh(pi)
    assert cos(-2*I) == cosh(2)

    assert cos(pi/2) == 0
    assert cos(-pi/2) == 0
    assert cos(pi/2) == 0
    assert cos(-pi/2) == 0
    assert cos((-3*10**73 + 1)*pi/2) == 0
    assert cos((7*10**103 + 1)*pi/2) == 0

    n = symbols('n', integer=True, even=False)
    e = symbols('e', even=True)
    assert cos(pi*n/2) == 0
    assert cos(pi*e/2) == (-1)**(e/2)

    assert cos(pi) == -1
    assert cos(-pi) == -1
    assert cos(2*pi) == 1
    assert cos(5*pi) == -1
    assert cos(8*pi) == 1

    assert cos(pi/3) == S.Half
    assert cos(pi*Rational(-2, 3)) == Rational(-1, 2)

    assert cos(pi/4) == S.Half*sqrt(2)
    assert cos(-pi/4) == S.Half*sqrt(2)
    assert cos(pi*Rational(11, 4)) == Rational(-1, 2)*sqrt(2)
    assert cos(pi*Rational(-3, 4)) == Rational(-1, 2)*sqrt(2)

    assert cos(pi/6) == S.Half*sqrt(3)
    assert cos(-pi/6) == S.Half*sqrt(3)
    assert cos(pi*Rational(7, 6)) == Rational(-1, 2)*sqrt(3)
    assert cos(pi*Rational(-5, 6)) == Rational(-1, 2)*sqrt(3)

    assert cos(pi*Rational(1, 5)) == (sqrt(5) + 1)/4
    assert cos(pi*Rational(2, 5)) == (sqrt(5) - 1)/4
    assert cos(pi*Rational(3, 5)) == -cos(pi*Rational(2, 5))
    assert cos(pi*Rational(4, 5)) == -cos(pi*Rational(1, 5))
    assert cos(pi*Rational(6, 5)) == -cos(pi*Rational(1, 5))
    assert cos(pi*Rational(8, 5)) == cos(pi*Rational(2, 5))

    assert cos(pi*Rational(-1273, 5)) == -cos(pi*Rational(2, 5))

    assert cos(pi/8) == sqrt((2 + sqrt(2))/4)

    assert cos(pi/12) == sqrt(2)/4 + sqrt(6)/4
    assert cos(pi*Rational(5, 12)) == -sqrt(2)/4 + sqrt(6)/4
    assert cos(pi*Rational(7, 12)) == sqrt(2)/4 - sqrt(6)/4
    assert cos(pi*Rational(11, 12)) == -sqrt(2)/4 - sqrt(6)/4

    assert cos(pi*Rational(104, 105)) == -cos(pi/105)
    assert cos(pi*Rational(106, 105)) == -cos(pi/105)

    assert cos(pi*Rational(-104, 105)) == -cos(pi/105)
    assert cos(pi*Rational(-106, 105)) == -cos(pi/105)

    assert cos(x*I) == cosh(x)
    assert cos(k*pi*I) == cosh(k*pi)

    assert cos(r).is_real is True

    assert cos(0, evaluate=False).is_algebraic
    assert cos(a).is_algebraic is None
    assert cos(na).is_algebraic is False
    q = Symbol('q', rational=True)
    assert cos(pi*q).is_algebraic
    assert cos(pi*Rational(2, 7)).is_algebraic

    assert cos(k*pi) == (-1)**k
    assert cos(2*k*pi) == 1
    assert cos(0, evaluate=False).is_zero is False
    assert cos(Rational(1, 2)).is_zero is False
    # The following test will return None as the result, but really it should
    # be True even if it is not always possible to resolve an assumptions query.
    assert cos(asin(-1, evaluate=False), evaluate=False).is_zero is None
    for d in list(range(1, 22)) + [60, 85]:
        for n in range(2*d + 1):
            x = n*pi/d
            e = abs( float(cos(x)) - cos(float(x)) )
            assert e < 1e-12

