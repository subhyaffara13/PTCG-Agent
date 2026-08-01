
def test_cot():
    R, x, y = puiseux_ring('x, y', QQ)
    assert rs_cot(x**6 + x**7, x, 8) == x**(-6) - x**(-5) + x**(-4) - \
        x**(-3) + x**(-2) - x**(-1) + 1 - x + x**2 - x**3 + x**4 - x**5 + \
        2*x**6/3 - 4*x**7/3
    assert rs_cot(x + x**2*y, x, 5) == -x**4*y**5 - x**4*y/15 + x**3*y**4 - \
        x**3/45 - x**2*y**3 - x**2*y/3 + x*y**2 - x/3 - y + x**(-1)


def test_cot():
    assert cot(nan) is nan

    assert cot.nargs == FiniteSet(1)
    assert cot(oo*I) == -I
    assert cot(-oo*I) == I
    assert cot(zoo) is nan

    assert cot(0) is zoo
    assert cot(2*pi) is zoo

    assert cot(acot(x)) == x
    assert cot(atan(x)) == 1 / x
    assert cot(asin(x)) == sqrt(1 - x**2) / x
    assert cot(acos(x)) == x / sqrt(1 - x**2)
    assert cot(acsc(x)) == sqrt(1 - 1 / x**2) * x
    assert cot(asec(x)) == 1 / (sqrt(1 - 1 / x**2) * x)
    assert cot(atan2(y, x)) == x/y

    assert cot(pi*I) == -coth(pi)*I
    assert cot(-pi*I) == coth(pi)*I
    assert cot(-2*I) == coth(2)*I

    assert cot(pi) == cot(2*pi) == cot(3*pi)
    assert cot(-pi) == cot(-2*pi) == cot(-3*pi)

    assert cot(pi/2) == 0
    assert cot(-pi/2) == 0
    assert cot(pi*Rational(5, 2)) == 0
    assert cot(pi*Rational(7, 2)) == 0

    assert cot(pi/3) == 1/sqrt(3)
    assert cot(pi*Rational(-2, 3)) == 1/sqrt(3)

    assert cot(pi/4) is S.One
    assert cot(-pi/4) is S.NegativeOne
    assert cot(pi*Rational(17, 4)) is S.One
    assert cot(pi*Rational(-3, 4)) is S.One

    assert cot(pi/6) == sqrt(3)
    assert cot(-pi/6) == -sqrt(3)
    assert cot(pi*Rational(7, 6)) == sqrt(3)
    assert cot(pi*Rational(-5, 6)) == sqrt(3)

    assert cot(pi/8) == 1 + sqrt(2)
    assert cot(pi*Rational(3, 8)) == -1 + sqrt(2)
    assert cot(pi*Rational(5, 8)) == 1 - sqrt(2)
    assert cot(pi*Rational(7, 8)) == -1 - sqrt(2)

    assert cot(pi/12) == sqrt(3) + 2
    assert cot(pi*Rational(5, 12)) == -sqrt(3) + 2
    assert cot(pi*Rational(7, 12)) == sqrt(3) - 2
    assert cot(pi*Rational(11, 12)) == -sqrt(3) - 2

    assert cot(pi/24).radsimp() == sqrt(2) + sqrt(3) + 2 + sqrt(6)
    assert cot(pi*Rational(5, 24)).radsimp() == -sqrt(2) - sqrt(3) + 2 + sqrt(6)
    assert cot(pi*Rational(7, 24)).radsimp() == -sqrt(2) + sqrt(3) - 2 + sqrt(6)
    assert cot(pi*Rational(11, 24)).radsimp() == sqrt(2) - sqrt(3) - 2 + sqrt(6)
    assert cot(pi*Rational(13, 24)).radsimp() == -sqrt(2) + sqrt(3) + 2 - sqrt(6)
    assert cot(pi*Rational(17, 24)).radsimp() == sqrt(2) - sqrt(3) + 2 - sqrt(6)
    assert cot(pi*Rational(19, 24)).radsimp() == sqrt(2) + sqrt(3) - 2 - sqrt(6)
    assert cot(pi*Rational(23, 24)).radsimp() == -sqrt(2) - sqrt(3) - 2 - sqrt(6)

    assert cot(x*I) == -coth(x)*I
    assert cot(k*pi*I) == -coth(k*pi)*I

    assert cot(r).is_real is None
    assert cot(r).is_extended_real is True

    assert cot(a).is_algebraic is None
    assert cot(na).is_algebraic is False

    assert cot(pi*Rational(10, 7)) == cot(pi*Rational(3, 7))
    assert cot(pi*Rational(11, 7)) == -cot(pi*Rational(3, 7))
    assert cot(pi*Rational(-11, 7)) == cot(pi*Rational(3, 7))

    assert cot(pi*Rational(39, 34)) == cot(pi*Rational(5, 34))
    assert cot(pi*Rational(-41, 34)) == -cot(pi*Rational(7, 34))

    assert cot(x).is_finite is None
    assert cot(r).is_finite is None
    i = Symbol('i', imaginary=True)
    assert cot(i).is_finite is True

    assert cot(x).subs(x, 3*pi) is zoo

    # https://github.com/sympy/sympy/issues/21177
    f = cot(pi*(x + 4))/(3*x)
    assert f.as_leading_term(x) == 1/(3*pi*x**2)

