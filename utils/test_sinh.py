import re

def test_sinh():
    R, x, y = ring('x, y', QQ)
    assert rs_sinh(x, x, 9) == x + x**3/6 + x**5/120 + x**7/5040
    assert rs_sinh(x*y + x**2*y**3, x, 9) == x**8*y**11/12 + \
        x**8*y**9/720 + x**7*y**9/12 + x**7*y**7/5040 + x**6*y**9/6 + \
        x**6*y**7/24 + x**5*y**7/2 + x**5*y**5/120 + x**4*y**5/2 + \
        x**3*y**3/6 + x**2*y**3 + x*y

    # constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', QQ[sinh(a), cosh(a), a])
    assert rs_sinh(x + a, x, 5) == 1/24*x**4*(sinh(a)) + 1/6*x**3*(cosh(a)) + 1/\
        2*x**2*(sinh(a)) + x*(cosh(a)) + (sinh(a))
    assert rs_sinh(x + x**2*y + a, x, 5) == 1/2*(sinh(a))*x**4*y**2 + 1/2*(cosh(a))\
        *x**4*y + 1/24*(sinh(a))*x**4 + (sinh(a))*x**3*y + 1/6*(cosh(a))*x**3 + \
        (cosh(a))*x**2*y + 1/2*(sinh(a))*x**2 + (cosh(a))*x + (sinh(a))

    R, x, y = ring('x, y', EX)
    assert rs_sinh(x + a, x, 5) == EX(sinh(a)/24)*x**4 + EX(cosh(a)/6)*x**3 + \
        EX(sinh(a)/2)*x**2 + EX(cosh(a))*x + EX(sinh(a))
    assert rs_sinh(x + x**2*y + a, x, 5) == EX(sinh(a)/2)*x**4*y**2 + EX(cosh(a)/\
        2)*x**4*y + EX(sinh(a)/24)*x**4 + EX(sinh(a))*x**3*y + EX(cosh(a)/6)*x**3 \
        + EX(cosh(a))*x**2*y + EX(sinh(a)/2)*x**2 + EX(cosh(a))*x + EX(sinh(a))


def test_sinh():
    a = sinh(interval(-1, 1))
    assert a.start == np.sinh(-1)
    assert a.end == np.sinh(1)

    a = sinh(1)
    assert a.start == np.sinh(1)
    assert a.end == np.sinh(1)


def test_sinh():
    x, y = symbols('x,y')

    k = Symbol('k', integer=True)

    assert sinh(nan) is nan
    assert sinh(zoo) is nan

    assert sinh(oo) is oo
    assert sinh(-oo) is -oo

    assert sinh(0) == 0

    assert unchanged(sinh, 1)
    assert sinh(-1) == -sinh(1)

    assert unchanged(sinh, x)
    assert sinh(-x) == -sinh(x)

    assert unchanged(sinh, pi)
    assert sinh(-pi) == -sinh(pi)

    assert unchanged(sinh, 2**1024 * E)
    assert sinh(-2**1024 * E) == -sinh(2**1024 * E)

    assert sinh(pi*I) == 0
    assert sinh(-pi*I) == 0
    assert sinh(2*pi*I) == 0
    assert sinh(-2*pi*I) == 0
    assert sinh(-3*10**73*pi*I) == 0
    assert sinh(7*10**103*pi*I) == 0

    assert sinh(pi*I/2) == I
    assert sinh(-pi*I/2) == -I
    assert sinh(pi*I*Rational(5, 2)) == I
    assert sinh(pi*I*Rational(7, 2)) == -I

    assert sinh(pi*I/3) == S.Half*sqrt(3)*I
    assert sinh(pi*I*Rational(-2, 3)) == Rational(-1, 2)*sqrt(3)*I

    assert sinh(pi*I/4) == S.Half*sqrt(2)*I
    assert sinh(-pi*I/4) == Rational(-1, 2)*sqrt(2)*I
    assert sinh(pi*I*Rational(17, 4)) == S.Half*sqrt(2)*I
    assert sinh(pi*I*Rational(-3, 4)) == Rational(-1, 2)*sqrt(2)*I

    assert sinh(pi*I/6) == S.Half*I
    assert sinh(-pi*I/6) == Rational(-1, 2)*I
    assert sinh(pi*I*Rational(7, 6)) == Rational(-1, 2)*I
    assert sinh(pi*I*Rational(-5, 6)) == Rational(-1, 2)*I

    assert sinh(pi*I/105) == sin(pi/105)*I
    assert sinh(-pi*I/105) == -sin(pi/105)*I

    assert unchanged(sinh, 2 + 3*I)

    assert sinh(x*I) == sin(x)*I

    assert sinh(k*pi*I) == 0
    assert sinh(17*k*pi*I) == 0

    assert sinh(k*pi*I/2) == sin(k*pi/2)*I

    assert sinh(x).as_real_imag(deep=False) == (cos(im(x))*sinh(re(x)),
                sin(im(x))*cosh(re(x)))
    x = Symbol('x', extended_real=True)
    assert sinh(x).as_real_imag(deep=False) == (sinh(x), 0)

    x = Symbol('x', real=True)
    assert sinh(I*x).is_finite is True
    assert sinh(x).is_real is True
    assert sinh(I).is_real is False
    p = Symbol('p', positive=True)
    assert sinh(p).is_zero is False
    assert sinh(0, evaluate=False).is_zero is True
    assert sinh(2*pi*I, evaluate=False).is_zero is True

