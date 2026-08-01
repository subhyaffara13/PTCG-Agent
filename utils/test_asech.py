
def test_asech():
    x = Symbol('x')

    assert unchanged(asech, -x)

    # values at fixed points
    assert asech(1) == 0
    assert asech(-1) == pi*I
    assert asech(0) is oo
    assert asech(2) == I*pi/3
    assert asech(-2) == 2*I*pi / 3
    assert asech(nan) is nan

    # at infinites
    assert asech(oo) == I*pi/2
    assert asech(-oo) == I*pi/2
    assert asech(zoo) == I*AccumBounds(-pi/2, pi/2)

    assert asech(I) == log(1 + sqrt(2)) - I*pi/2
    assert asech(-I) == log(1 + sqrt(2)) + I*pi/2
    assert asech(sqrt(2) - sqrt(6)) == 11*I*pi / 12
    assert asech(sqrt(2 - 2/sqrt(5))) == I*pi / 10
    assert asech(-sqrt(2 - 2/sqrt(5))) == 9*I*pi / 10
    assert asech(2 / sqrt(2 + sqrt(2))) == I*pi / 8
    assert asech(-2 / sqrt(2 + sqrt(2))) == 7*I*pi / 8
    assert asech(sqrt(5) - 1) == I*pi / 5
    assert asech(1 - sqrt(5)) == 4*I*pi / 5
    assert asech(-sqrt(2*(2 + sqrt(2)))) == 5*I*pi / 8

    # properties
    # asech(x) == acosh(1/x)
    assert asech(sqrt(2)) == acosh(1/sqrt(2))
    assert asech(2/sqrt(3)) == acosh(sqrt(3)/2)
    assert asech(2/sqrt(2 + sqrt(2))) == acosh(sqrt(2 + sqrt(2))/2)
    assert asech(2) == acosh(S.Half)

    # reality
    assert asech(S(2)).is_real is False
    assert asech(-S(1) / 3).is_real is False
    assert asech(S(2) / 3).is_finite is True
    assert asech(S(0)).is_real is False
    assert asech(S(0)).is_extended_real is True
    assert asech(symbols('y', real=True)).is_real is None

    # asech(x) == I*acos(1/x)
    # (Note: the exact formula is asech(x) == +/- I*acos(1/x))
    assert asech(-sqrt(2)) == I*acos(-1/sqrt(2))
    assert asech(-2/sqrt(3)) == I*acos(-sqrt(3)/2)
    assert asech(-S(2)) == I*acos(Rational(-1, 2))
    assert asech(-2/sqrt(2)) == I*acos(-sqrt(2)/2)

    # sech(asech(x)) / x == 1
    assert expand_mul(sech(asech(sqrt(6) - sqrt(2))) / (sqrt(6) - sqrt(2))) == 1
    assert expand_mul(sech(asech(sqrt(6) + sqrt(2))) / (sqrt(6) + sqrt(2))) == 1
    assert (sech(asech(sqrt(2 + 2/sqrt(5)))) / (sqrt(2 + 2/sqrt(5)))).simplify() == 1
    assert (sech(asech(-sqrt(2 + 2/sqrt(5)))) / (-sqrt(2 + 2/sqrt(5)))).simplify() == 1
    assert (sech(asech(sqrt(2*(2 + sqrt(2))))) / (sqrt(2*(2 + sqrt(2))))).simplify() == 1
    assert expand_mul(sech(asech(1 + sqrt(5))) / (1 + sqrt(5))) == 1
    assert expand_mul(sech(asech(-1 - sqrt(5))) / (-1 - sqrt(5))) == 1
    assert expand_mul(sech(asech(-sqrt(6) - sqrt(2))) / (-sqrt(6) - sqrt(2))) == 1

    # numerical evaluation
    assert str(asech(5*I).n(6)) == '0.19869 - 1.5708*I'
    assert str(asech(-5*I).n(6)) == '0.19869 + 1.5708*I'

