import re

def test_sin():
    f = lambdify(x, sin(x)**2)
    assert isinstance(f(2), float)
    f = lambdify(x, sin(x)**2, modules="math")
    assert isinstance(f(2), float)


def test_sin():
    e = sin(x).lseries(x)
    assert next(e) == x
    assert next(e) == -x**3/6
    assert next(e) == x**5/120


def test_sin():
    assert sin(8*x).nseries(x, n=4) == 8*x - 256*x**3/3 + O(x**4)
    assert sin(x + y).nseries(x, n=1) == sin(y) + O(x)
    assert sin(x + y).nseries(x, n=2) == sin(y) + cos(y)*x + O(x**2)
    assert sin(x + y).nseries(x, n=5) == sin(y) + cos(y)*x - sin(y)*x**2/2 - \
        cos(y)*x**3/6 + sin(y)*x**4/24 + O(x**5)


def test_sin():
    e1 = sin(x).series(x, 0)
    e2 = series(sin(x), x, 0)
    assert e1 == e2


def test_sin():
    R, x, y = ring('x, y', QQ)
    assert rs_sin(x, x, 9) == x - x**3/6 + x**5/120 - x**7/5040
    assert rs_sin(x*y + x**2*y**3, x, 9) == x**8*y**11/12 - \
        x**8*y**9/720 + x**7*y**9/12 - x**7*y**7/5040 - x**6*y**9/6 + \
        x**6*y**7/24 - x**5*y**7/2 + x**5*y**5/120 - x**4*y**5/2 - \
        x**3*y**3/6 + x**2*y**3 + x*y

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', QQ[sin(a), cos(a), a])
    assert rs_sin(x + a, x, 5) == sin(a)*x**4/24 - cos(a)*x**3/6 - \
        sin(a)*x**2/2 + cos(a)*x + sin(a)
    assert rs_sin(x + x**2*y + a, x, 5) == -sin(a)*x**4*y**2/2 - \
        cos(a)*x**4*y/2 + sin(a)*x**4/24 - sin(a)*x**3*y - cos(a)*x**3/6 + \
        cos(a)*x**2*y - sin(a)*x**2/2 + cos(a)*x + sin(a)

    R, x, y = ring('x, y', EX)
    assert rs_sin(x + a, x, 5) == EX(sin(a)/24)*x**4 - EX(cos(a)/6)*x**3 - \
        EX(sin(a)/2)*x**2 + EX(cos(a))*x + EX(sin(a))
    assert rs_sin(x + x**2*y + a, x, 5) == -EX(sin(a)/2)*x**4*y**2 - \
        EX(cos(a)/2)*x**4*y + EX(sin(a)/24)*x**4 - EX(sin(a))*x**3*y - \
        EX(cos(a)/6)*x**3 + EX(cos(a))*x**2*y - EX(sin(a)/2)*x**2 + \
        EX(cos(a))*x + EX(sin(a))


def test_sin():
    a = sin(interval(0, np.pi / 4))
    assert a.start == np.sin(0)
    assert a.end == np.sin(np.pi / 4)

    a = sin(interval(-np.pi / 4, np.pi / 4))
    assert a.start == np.sin(-np.pi / 4)
    assert a.end == np.sin(np.pi / 4)

    a = sin(interval(np.pi / 4, 3 * np.pi / 4))
    assert a.start == np.sin(np.pi / 4)
    assert a.end == 1

    a = sin(interval(7 * np.pi / 6, 7 * np.pi / 4))
    assert a.start == -1
    assert a.end == np.sin(7 * np.pi / 6)

    a = sin(interval(0, 3 * np.pi))
    assert a.start == -1
    assert a.end == 1

    a = sin(interval(np.pi / 3, 7 * np.pi / 4))
    assert a.start == -1
    assert a.end == 1

    a = sin(np.pi / 4)
    assert a.start == np.sin(np.pi / 4)
    assert a.end == np.sin(np.pi / 4)

    a = sin(interval(1, 2, is_valid=False))
    assert a.is_valid is False


def test_sin():
    x, y = symbols('x y')
    z = symbols('z', imaginary=True)

    assert sin.nargs == FiniteSet(1)
    assert sin(nan) is nan
    assert sin(zoo) is nan

    assert sin(oo) == AccumBounds(-1, 1)
    assert sin(oo) - sin(oo) == AccumBounds(-2, 2)
    assert sin(oo*I) == oo*I
    assert sin(-oo*I) == -oo*I
    assert 0*sin(oo) is S.Zero
    assert 0/sin(oo) is S.Zero
    assert 0 + sin(oo) == AccumBounds(-1, 1)
    assert 5 + sin(oo) == AccumBounds(4, 6)

    assert sin(0) == 0

    assert sin(z*I) == I*sinh(z)
    assert sin(asin(x)) == x
    assert sin(atan(x)) == x / sqrt(1 + x**2)
    assert sin(acos(x)) == sqrt(1 - x**2)
    assert sin(acot(x)) == 1 / (sqrt(1 + 1 / x**2) * x)
    assert sin(acsc(x)) == 1 / x
    assert sin(asec(x)) == sqrt(1 - 1 / x**2)
    assert sin(atan2(y, x)) == y / sqrt(x**2 + y**2)

    assert sin(pi*I) == sinh(pi)*I
    assert sin(-pi*I) == -sinh(pi)*I
    assert sin(-2*I) == -sinh(2)*I

    assert sin(pi) == 0
    assert sin(-pi) == 0
    assert sin(2*pi) == 0
    assert sin(-2*pi) == 0
    assert sin(-3*10**73*pi) == 0
    assert sin(7*10**103*pi) == 0

    assert sin(pi/2) == 1
    assert sin(-pi/2) == -1
    assert sin(pi*Rational(5, 2)) == 1
    assert sin(pi*Rational(7, 2)) == -1

    ne = symbols('ne', integer=True, even=False)
    e = symbols('e', even=True)
    assert sin(pi*ne/2) == (-1)**(ne/2 - S.Half)
    assert sin(pi*k/2).func == sin
    assert sin(pi*e/2) == 0
    assert sin(pi*k) == 0
    assert sin(pi*k).subs(k, 3) == sin(pi*k/2).subs(k, 6)  # issue 8298

    assert sin(pi/3) == S.Half*sqrt(3)
    assert sin(pi*Rational(-2, 3)) == Rational(-1, 2)*sqrt(3)

    assert sin(pi/4) == S.Half*sqrt(2)
    assert sin(-pi/4) == Rational(-1, 2)*sqrt(2)
    assert sin(pi*Rational(17, 4)) == S.Half*sqrt(2)
    assert sin(pi*Rational(-3, 4)) == Rational(-1, 2)*sqrt(2)

    assert sin(pi/6) == S.Half
    assert sin(-pi/6) == Rational(-1, 2)
    assert sin(pi*Rational(7, 6)) == Rational(-1, 2)
    assert sin(pi*Rational(-5, 6)) == Rational(-1, 2)

    assert sin(pi*Rational(1, 5)) == sqrt((5 - sqrt(5)) / 8)
    assert sin(pi*Rational(2, 5)) == sqrt((5 + sqrt(5)) / 8)
    assert sin(pi*Rational(3, 5)) == sin(pi*Rational(2, 5))
    assert sin(pi*Rational(4, 5)) == sin(pi*Rational(1, 5))
    assert sin(pi*Rational(6, 5)) == -sin(pi*Rational(1, 5))
    assert sin(pi*Rational(8, 5)) == -sin(pi*Rational(2, 5))

    assert sin(pi*Rational(-1273, 5)) == -sin(pi*Rational(2, 5))

    assert sin(pi/8) == sqrt((2 - sqrt(2))/4)

    assert sin(pi/10) == Rational(-1, 4) + sqrt(5)/4

    assert sin(pi/12) == -sqrt(2)/4 + sqrt(6)/4
    assert sin(pi*Rational(5, 12)) == sqrt(2)/4 + sqrt(6)/4
    assert sin(pi*Rational(-7, 12)) == -sqrt(2)/4 - sqrt(6)/4
    assert sin(pi*Rational(-11, 12)) == sqrt(2)/4 - sqrt(6)/4

    assert sin(pi*Rational(104, 105)) == sin(pi/105)
    assert sin(pi*Rational(106, 105)) == -sin(pi/105)

    assert sin(pi*Rational(-104, 105)) == -sin(pi/105)
    assert sin(pi*Rational(-106, 105)) == sin(pi/105)

    assert sin(x*I) == sinh(x)*I

    assert sin(k*pi) == 0
    assert sin(17*k*pi) == 0
    assert sin(2*k*pi + 4) == sin(4)
    assert sin(2*k*pi + m*pi + 1) == (-1)**(m + 2*k)*sin(1)

    assert sin(k*pi*I) == sinh(k*pi)*I

    assert sin(r).is_real is True

    assert sin(0, evaluate=False).is_algebraic
    assert sin(a).is_algebraic is None
    assert sin(na).is_algebraic is False
    q = Symbol('q', rational=True)
    assert sin(pi*q).is_algebraic
    qn = Symbol('qn', rational=True, nonzero=True)
    assert sin(qn).is_rational is False
    assert sin(q).is_rational is None  # issue 8653

    assert isinstance(sin( re(x) - im(y)), sin) is True
    assert isinstance(sin(-re(x) + im(y)), sin) is False

    assert sin(SetExpr(Interval(0, 1))) == SetExpr(ImageSet(Lambda(x, sin(x)),
                       Interval(0, 1)))

    for d in list(range(1, 22)) + [60, 85]:
        for n in range(d*2 + 1):
            x = n*pi/d
            e = abs( float(sin(x)) - sin(float(x)) )
            assert e < 1e-12

    assert sin(0, evaluate=False).is_zero is True
    assert sin(k*pi, evaluate=False).is_zero is True

    assert sin(Add(1, -1, evaluate=False), evaluate=False).is_zero is True

