
def test_acot():
    assert acot(nan) is nan

    assert acot.nargs == FiniteSet(1)
    assert acot(-oo) == 0
    assert acot(oo) == 0
    assert acot(zoo) == 0
    assert acot(1) == pi/4
    assert acot(0) == pi/2
    assert acot(sqrt(3)/3) == pi/3
    assert acot(1/sqrt(3)) == pi/3
    assert acot(-1/sqrt(3)) == -pi/3
    assert acot(x).diff(x) == -1/(1 + x**2)

    assert acot(r).is_extended_real is True

    assert acot(I*pi) == -I*acoth(pi)
    assert acot(-2*I) == I*acoth(2)
    assert acot(x).is_positive is None
    assert acot(n).is_positive is False
    assert acot(p).is_positive is True
    assert acot(I).is_positive is False
    assert acot(Rational(1, 4)).is_rational is False
    assert unchanged(acot, cot(x))
    assert unchanged(acot, tan(x))
    assert acot(cot(Rational(1, 4))) == Rational(1, 4)
    assert acot(tan(Rational(-1, 4))) == Rational(1, 4) - pi/2

