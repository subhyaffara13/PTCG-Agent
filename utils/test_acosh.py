
def test_acosh():
    a = acosh(interval(3, 5))
    assert a.start == np.arccosh(3)
    assert a.end == np.arccosh(5)

    a = acosh(interval(0, 3))
    assert a.is_valid is None
    a = acosh(interval(-3, 0.5))
    assert a.is_valid is False

    a = acosh(0.5)
    assert a.is_valid is False

    a = acosh(2)
    assert a.start == np.arccosh(2)
    assert a.end == np.arccosh(2)


def test_acosh():
    x = Symbol('x')

    assert unchanged(acosh, -x)

    #at specific points
    assert acosh(1) == 0
    assert acosh(-1) == pi*I
    assert acosh(0) == I*pi/2
    assert acosh(S.Half) == I*pi/3
    assert acosh(Rational(-1, 2)) == pi*I*Rational(2, 3)
    assert acosh(nan) is nan

    # at infinites
    assert acosh(oo) is oo
    assert acosh(-oo) is oo

    assert acosh(I*oo) == oo + I*pi/2
    assert acosh(-I*oo) == oo - I*pi/2

    assert acosh(zoo) is zoo

    assert acosh(I) == log(I*(1 + sqrt(2)))
    assert acosh(-I) == log(-I*(1 + sqrt(2)))
    assert acosh((sqrt(3) - 1)/(2*sqrt(2))) == pi*I*Rational(5, 12)
    assert acosh(-(sqrt(3) - 1)/(2*sqrt(2))) == pi*I*Rational(7, 12)
    assert acosh(sqrt(2)/2) == I*pi/4
    assert acosh(-sqrt(2)/2) == I*pi*Rational(3, 4)
    assert acosh(sqrt(3)/2) == I*pi/6
    assert acosh(-sqrt(3)/2) == I*pi*Rational(5, 6)
    assert acosh(sqrt(2 + sqrt(2))/2) == I*pi/8
    assert acosh(-sqrt(2 + sqrt(2))/2) == I*pi*Rational(7, 8)
    assert acosh(sqrt(2 - sqrt(2))/2) == I*pi*Rational(3, 8)
    assert acosh(-sqrt(2 - sqrt(2))/2) == I*pi*Rational(5, 8)
    assert acosh((1 + sqrt(3))/(2*sqrt(2))) == I*pi/12
    assert acosh(-(1 + sqrt(3))/(2*sqrt(2))) == I*pi*Rational(11, 12)
    assert acosh((sqrt(5) + 1)/4) == I*pi/5
    assert acosh(-(sqrt(5) + 1)/4) == I*pi*Rational(4, 5)

    assert str(acosh(5*I).n(6)) == '2.31244 + 1.5708*I'
    assert str(acosh(-5*I).n(6)) == '2.31244 - 1.5708*I'

    # inverse composition
    assert unchanged(acosh, Symbol('v1'))

    assert acosh(cosh(-3, evaluate=False)) == 3
    assert acosh(cosh(3, evaluate=False)) == 3
    assert acosh(cosh(0, evaluate=False)) == 0
    assert acosh(cosh(I, evaluate=False)) == I
    assert acosh(cosh(-I, evaluate=False)) == I
    assert acosh(cosh(7*I, evaluate=False)) == -2*I*pi + 7*I
    assert acosh(cosh(1 + I)) == 1 + I
    assert acosh(cosh(3 - 3*I)) == 3 - 3*I
    assert acosh(cosh(-3 + 2*I)) == 3 - 2*I
    assert acosh(cosh(-5 - 17*I)) == 5 - 6*I*pi + 17*I
    assert acosh(cosh(-21 + 11*I)) == 21 - 11*I + 4*I*pi
    assert acosh(cosh(cosh(1) + I)) == cosh(1) + I
    assert acosh(1, evaluate=False).is_zero is True

    # Reality
    assert acosh(S(2)).is_real is True
    assert acosh(S(2)).is_extended_real is True
    assert acosh(oo).is_extended_real is True
    assert acosh(S(2)).is_finite is True
    assert acosh(S(1) / 5).is_real is False
    assert (acosh(2) - oo) == -oo
    assert acosh(symbols('y', real=True)).is_real is None

