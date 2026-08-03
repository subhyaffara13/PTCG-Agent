import re

def test_cosh():
    R, x, y = ring('x, y', QQ)
    assert rs_cosh(x, x, 9) == 1 + x**2/2 + x**4/24 + x**6/720 + x**8/40320
    assert rs_cosh(x*y + x**2*y**3, x, 9) == x**8*y**12/24 + \
        x**8*y**10/48 + x**8*y**8/40320 + x**7*y**10/6 + \
        x**7*y**8/120 + x**6*y**8/4 + x**6*y**6/720 + x**5*y**6/6 + \
        x**4*y**6/2 + x**4*y**4/24 + x**3*y**4 + x**2*y**2/2 + 1

    # constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', QQ[sinh(a), cosh(a), a])
    assert rs_cosh(x + a, x, 5) == 1/24*(cosh(a))*x**4 + 1/6*(sinh(a))*x**3 + \
        1/2*(cosh(a))*x**2 + (sinh(a))*x + (cosh(a))
    assert rs_cosh(x + x**2*y + a, x, 5) == 1/2*(cosh(a))*x**4*y**2 + 1/2*(sinh(a))\
        *x**4*y + 1/24*(cosh(a))*x**4 + (cosh(a))*x**3*y + 1/6*(sinh(a))*x**3 + \
        (sinh(a))*x**2*y + 1/2*(cosh(a))*x**2 + (sinh(a))*x + (cosh(a))
    R, x, y = ring('x, y', EX)
    assert rs_cosh(x + a, x, 5) == EX(cosh(a)/24)*x**4 + EX(sinh(a)/6)*x**3 + \
        EX(cosh(a)/2)*x**2 + EX(sinh(a))*x + EX(cosh(a))
    assert rs_cosh(x + x**2*y + a, x, 5) == EX(cosh(a)/2)*x**4*y**2 + EX(sinh(a)/\
        2)*x**4*y + EX(cosh(a)/24)*x**4 + EX(cosh(a))*x**3*y + EX(sinh(a)/6)*x**3 \
        + EX(sinh(a))*x**2*y + EX(cosh(a)/2)*x**2 + EX(sinh(a))*x + EX(cosh(a))


def test_cosh():
    a = cosh(interval(1, 2))
    assert a.start == np.cosh(1)
    assert a.end == np.cosh(2)
    a = cosh(interval(-2, -1))
    assert a.start == np.cosh(-1)
    assert a.end == np.cosh(-2)

    a = cosh(interval(-2, 1))
    assert a.start == 1
    assert a.end == np.cosh(-2)

    a = cosh(1)
    assert a.start == np.cosh(1)
    assert a.end == np.cosh(1)


def test_cosh():
    x, y = symbols('x,y')

    k = Symbol('k', integer=True)

    assert cosh(nan) is nan
    assert cosh(zoo) is nan

    assert cosh(oo) is oo
    assert cosh(-oo) is oo

    assert cosh(0) == 1

    assert unchanged(cosh, 1)
    assert cosh(-1) == cosh(1)

    assert unchanged(cosh, x)
    assert cosh(-x) == cosh(x)

    assert cosh(pi*I) == cos(pi)
    assert cosh(-pi*I) == cos(pi)

    assert unchanged(cosh, 2**1024 * E)
    assert cosh(-2**1024 * E) == cosh(2**1024 * E)

    assert cosh(pi*I/2) == 0
    assert cosh(-pi*I/2) == 0
    assert cosh((-3*10**73 + 1)*pi*I/2) == 0
    assert cosh((7*10**103 + 1)*pi*I/2) == 0

    assert cosh(pi*I) == -1
    assert cosh(-pi*I) == -1
    assert cosh(5*pi*I) == -1
    assert cosh(8*pi*I) == 1

    assert cosh(pi*I/3) == S.Half
    assert cosh(pi*I*Rational(-2, 3)) == Rational(-1, 2)

    assert cosh(pi*I/4) == S.Half*sqrt(2)
    assert cosh(-pi*I/4) == S.Half*sqrt(2)
    assert cosh(pi*I*Rational(11, 4)) == Rational(-1, 2)*sqrt(2)
    assert cosh(pi*I*Rational(-3, 4)) == Rational(-1, 2)*sqrt(2)

    assert cosh(pi*I/6) == S.Half*sqrt(3)
    assert cosh(-pi*I/6) == S.Half*sqrt(3)
    assert cosh(pi*I*Rational(7, 6)) == Rational(-1, 2)*sqrt(3)
    assert cosh(pi*I*Rational(-5, 6)) == Rational(-1, 2)*sqrt(3)

    assert cosh(pi*I/105) == cos(pi/105)
    assert cosh(-pi*I/105) == cos(pi/105)

    assert unchanged(cosh, 2 + 3*I)

    assert cosh(x*I) == cos(x)

    assert cosh(k*pi*I) == cos(k*pi)
    assert cosh(17*k*pi*I) == cos(17*k*pi)

    assert unchanged(cosh, k*pi)

    assert cosh(x).as_real_imag(deep=False) == (cos(im(x))*cosh(re(x)),
                sin(im(x))*sinh(re(x)))
    x = Symbol('x', extended_real=True)
    assert cosh(x).as_real_imag(deep=False) == (cosh(x), 0)

    x = Symbol('x', real=True)
    assert cosh(I*x).is_finite is True
    assert cosh(I*x).is_real is True
    assert cosh(I*2 + 1).is_real is False
    assert cosh(5*I*S.Pi/2, evaluate=False).is_zero is True
    assert cosh(x).is_zero is False

