import re

def test_tanh():
    R, x, y = ring('x, y', QQ)
    assert rs_tanh(x, x, 9) == x - QQ(1,3)*x**3 + QQ(2,15)*x**5 - QQ(17,315)*x**7
    assert rs_tanh(x*y + x**2*y**3, x, 9) == 4*x**8*y**11/3 - \
        17*x**8*y**9/45 + 4*x**7*y**9/3 - 17*x**7*y**7/315 - x**6*y**9/3 + \
        2*x**6*y**7/3 - x**5*y**7 + 2*x**5*y**5/15 - x**4*y**5 - \
        x**3*y**3/3 + x**2*y**3 + x*y

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', EX)
    assert rs_tanh(x + a, x, 5) == EX(tanh(a)**5 - 5*tanh(a)**3/3 +
        2*tanh(a)/3)*x**4 + EX(-tanh(a)**4 + 4*tanh(a)**2/3 - QQ(1, 3))*x**3 + \
        EX(tanh(a)**3 - tanh(a))*x**2 + EX(-tanh(a)**2 + 1)*x + EX(tanh(a))

    p = rs_tanh(x + x**2*y + a, x, 4)
    assert (p.compose(x, 10)).compose(y, 5) == EX(-1000*tanh(a)**4 + \
        10100*tanh(a)**3 + 2470*tanh(a)**2/3 - 10099*tanh(a) + QQ(530, 3))


def test_tanh():
    a = tanh(interval(-3, 3))
    assert a.start == np.tanh(-3)
    assert a.end == np.tanh(3)

    a = tanh(3)
    assert a.start == np.tanh(3)
    assert a.end == np.tanh(3)


def test_tanh():
    x, y = symbols('x,y')

    k = Symbol('k', integer=True)

    assert tanh(nan) is nan
    assert tanh(zoo) is nan

    assert tanh(oo) == 1
    assert tanh(-oo) == -1

    assert tanh(0) == 0

    assert unchanged(tanh, 1)
    assert tanh(-1) == -tanh(1)

    assert unchanged(tanh, x)
    assert tanh(-x) == -tanh(x)

    assert unchanged(tanh, pi)
    assert tanh(-pi) == -tanh(pi)

    assert unchanged(tanh, 2**1024 * E)
    assert tanh(-2**1024 * E) == -tanh(2**1024 * E)

    assert tanh(pi*I) == 0
    assert tanh(-pi*I) == 0
    assert tanh(2*pi*I) == 0
    assert tanh(-2*pi*I) == 0
    assert tanh(-3*10**73*pi*I) == 0
    assert tanh(7*10**103*pi*I) == 0

    assert tanh(pi*I/2) is zoo
    assert tanh(-pi*I/2) is zoo
    assert tanh(pi*I*Rational(5, 2)) is zoo
    assert tanh(pi*I*Rational(7, 2)) is zoo

    assert tanh(pi*I/3) == sqrt(3)*I
    assert tanh(pi*I*Rational(-2, 3)) == sqrt(3)*I

    assert tanh(pi*I/4) == I
    assert tanh(-pi*I/4) == -I
    assert tanh(pi*I*Rational(17, 4)) == I
    assert tanh(pi*I*Rational(-3, 4)) == I

    assert tanh(pi*I/6) == I/sqrt(3)
    assert tanh(-pi*I/6) == -I/sqrt(3)
    assert tanh(pi*I*Rational(7, 6)) == I/sqrt(3)
    assert tanh(pi*I*Rational(-5, 6)) == I/sqrt(3)

    assert tanh(pi*I/105) == tan(pi/105)*I
    assert tanh(-pi*I/105) == -tan(pi/105)*I

    assert unchanged(tanh, 2 + 3*I)

    assert tanh(x*I) == tan(x)*I

    assert tanh(k*pi*I) == 0
    assert tanh(17*k*pi*I) == 0

    assert tanh(k*pi*I/2) == tan(k*pi/2)*I

    assert tanh(x).as_real_imag(deep=False) == (sinh(re(x))*cosh(re(x))/(cos(im(x))**2
                                + sinh(re(x))**2),
                                sin(im(x))*cos(im(x))/(cos(im(x))**2 + sinh(re(x))**2))
    x = Symbol('x', extended_real=True)
    assert tanh(x).as_real_imag(deep=False) == (tanh(x), 0)
    assert tanh(I*pi/3 + 1).is_real is False
    assert tanh(x).is_real is True
    assert tanh(I*pi*x/2).is_real is None


def test_tanh():
    mp.dps = 15
    assert tanh(0) == 0
    assert tanh(inf) == 1
    assert tanh(-inf) == -1
    assert isnan(tanh(nan))
    assert tanh(mpc('inf', '0')) == 1

