
def test_tan():
    R, x, y = ring('x, y', QQ)
    assert rs_tan(x, x, 9) == x + x**3/3 + QQ(2,15)*x**5 + QQ(17,315)*x**7
    assert rs_tan(x*y + x**2*y**3, x, 9) == 4*x**8*y**11/3 + 17*x**8*y**9/45 + \
        4*x**7*y**9/3 + 17*x**7*y**7/315 + x**6*y**9/3 + 2*x**6*y**7/3 + \
        x**5*y**7 + 2*x**5*y**5/15 + x**4*y**5 + x**3*y**3/3 + x**2*y**3 + x*y

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', QQ[tan(a), a])
    assert rs_tan(x + a, x, 5) == (tan(a)**5 + 5*tan(a)**3/3 +
        2*tan(a)/3)*x**4 + (tan(a)**4 + 4*tan(a)**2/3 + Rational(1, 3))*x**3 + \
        (tan(a)**3 + tan(a))*x**2 + (tan(a)**2 + 1)*x + tan(a)
    assert rs_tan(x + x**2*y + a, x, 4) == (2*tan(a)**3 + 2*tan(a))*x**3*y + \
        (tan(a)**4 + Rational(4, 3)*tan(a)**2 + Rational(1, 3))*x**3 + (tan(a)**2 + 1)*x**2*y + \
        (tan(a)**3 + tan(a))*x**2 + (tan(a)**2 + 1)*x + tan(a)

    R, x, y = ring('x, y', EX)
    assert rs_tan(x + a, x, 5) == EX(tan(a)**5 + 5*tan(a)**3/3 +
        2*tan(a)/3)*x**4 + EX(tan(a)**4 + 4*tan(a)**2/3 + EX(1)/3)*x**3 + \
        EX(tan(a)**3 + tan(a))*x**2 + EX(tan(a)**2 + 1)*x + EX(tan(a))
    assert rs_tan(x + x**2*y + a, x, 4) == EX(2*tan(a)**3 +
        2*tan(a))*x**3*y + EX(tan(a)**4 + 4*tan(a)**2/3 + EX(1)/3)*x**3 + \
        EX(tan(a)**2 + 1)*x**2*y + EX(tan(a)**3 + tan(a))*x**2 + \
        EX(tan(a)**2 + 1)*x + EX(tan(a))

    p = x + x**2 + 5
    assert rs_atan(p, x, 10).compose(x, 10) == EX(atan(5) + S(67701870330562640) / \
        668083460499)


def test_tan():
    a = tan(interval(0, np.pi / 4))
    assert a.start == 0
    # must match lib_interval definition of tan:
    assert a.end == np.sin(np.pi / 4)/np.cos(np.pi / 4)

    a = tan(interval(np.pi / 4, 3 * np.pi / 4))
    #discontinuity
    assert a.is_valid is None


def test_tan():
    assert tan(nan) is nan

    assert tan(zoo) is nan
    assert tan(oo) == AccumBounds(-oo, oo)
    assert tan(oo) - tan(oo) == AccumBounds(-oo, oo)
    assert tan.nargs == FiniteSet(1)
    assert tan(oo*I) == I
    assert tan(-oo*I) == -I

    assert tan(0) == 0

    assert tan(atan(x)) == x
    assert tan(asin(x)) == x / sqrt(1 - x**2)
    assert tan(acos(x)) == sqrt(1 - x**2) / x
    assert tan(acot(x)) == 1 / x
    assert tan(acsc(x)) == 1 / (sqrt(1 - 1 / x**2) * x)
    assert tan(asec(x)) == sqrt(1 - 1 / x**2) * x
    assert tan(atan2(y, x)) == y/x

    assert tan(pi*I) == tanh(pi)*I
    assert tan(-pi*I) == -tanh(pi)*I
    assert tan(-2*I) == -tanh(2)*I

    assert tan(pi) == 0
    assert tan(-pi) == 0
    assert tan(2*pi) == 0
    assert tan(-2*pi) == 0
    assert tan(-3*10**73*pi) == 0

    assert tan(pi/2) is zoo
    assert tan(pi*Rational(3, 2)) is zoo

    assert tan(pi/3) == sqrt(3)
    assert tan(pi*Rational(-2, 3)) == sqrt(3)

    assert tan(pi/4) is S.One
    assert tan(-pi/4) is S.NegativeOne
    assert tan(pi*Rational(17, 4)) is S.One
    assert tan(pi*Rational(-3, 4)) is S.One

    assert tan(pi/5) == sqrt(5 - 2*sqrt(5))
    assert tan(pi*Rational(2, 5)) == sqrt(5 + 2*sqrt(5))
    assert tan(pi*Rational(18, 5)) == -sqrt(5 + 2*sqrt(5))
    assert tan(pi*Rational(-16, 5)) == -sqrt(5 - 2*sqrt(5))

    assert tan(pi/6) == 1/sqrt(3)
    assert tan(-pi/6) == -1/sqrt(3)
    assert tan(pi*Rational(7, 6)) == 1/sqrt(3)
    assert tan(pi*Rational(-5, 6)) == 1/sqrt(3)

    assert tan(pi/8) == -1 + sqrt(2)
    assert tan(pi*Rational(3, 8)) == 1 + sqrt(2)  # issue 15959
    assert tan(pi*Rational(5, 8)) == -1 - sqrt(2)
    assert tan(pi*Rational(7, 8)) == 1 - sqrt(2)

    assert tan(pi/10) == sqrt(1 - 2*sqrt(5)/5)
    assert tan(pi*Rational(3, 10)) == sqrt(1 + 2*sqrt(5)/5)
    assert tan(pi*Rational(17, 10)) == -sqrt(1 + 2*sqrt(5)/5)
    assert tan(pi*Rational(-31, 10)) == -sqrt(1 - 2*sqrt(5)/5)

    assert tan(pi/12) == -sqrt(3) + 2
    assert tan(pi*Rational(5, 12)) == sqrt(3) + 2
    assert tan(pi*Rational(7, 12)) == -sqrt(3) - 2
    assert tan(pi*Rational(11, 12)) == sqrt(3) - 2

    assert tan(pi/24).radsimp() == -2 - sqrt(3) + sqrt(2) + sqrt(6)
    assert tan(pi*Rational(5, 24)).radsimp() == -2 + sqrt(3) - sqrt(2) + sqrt(6)
    assert tan(pi*Rational(7, 24)).radsimp() == 2 - sqrt(3) - sqrt(2) + sqrt(6)
    assert tan(pi*Rational(11, 24)).radsimp() == 2 + sqrt(3) + sqrt(2) + sqrt(6)
    assert tan(pi*Rational(13, 24)).radsimp() == -2 - sqrt(3) - sqrt(2) - sqrt(6)
    assert tan(pi*Rational(17, 24)).radsimp() == -2 + sqrt(3) + sqrt(2) - sqrt(6)
    assert tan(pi*Rational(19, 24)).radsimp() == 2 - sqrt(3) + sqrt(2) - sqrt(6)
    assert tan(pi*Rational(23, 24)).radsimp() == 2 + sqrt(3) - sqrt(2) - sqrt(6)

    assert tan(x*I) == tanh(x)*I

    assert tan(k*pi) == 0
    assert tan(17*k*pi) == 0

    assert tan(k*pi*I) == tanh(k*pi)*I

    assert tan(r).is_real is None
    assert tan(r).is_extended_real is True

    assert tan(0, evaluate=False).is_algebraic
    assert tan(a).is_algebraic is None
    assert tan(na).is_algebraic is False

    assert tan(pi*Rational(10, 7)) == tan(pi*Rational(3, 7))
    assert tan(pi*Rational(11, 7)) == -tan(pi*Rational(3, 7))
    assert tan(pi*Rational(-11, 7)) == tan(pi*Rational(3, 7))

    assert tan(pi*Rational(15, 14)) == tan(pi/14)
    assert tan(pi*Rational(-15, 14)) == -tan(pi/14)

    assert tan(r).is_finite is None
    assert tan(I*r).is_finite is True

    # https://github.com/sympy/sympy/issues/21177
    f = tan(pi*(x + S(3)/2))/(3*x)
    assert f.as_leading_term(x) == -1/(3*pi*x**2)

