
def test_acos():
    a = acos(interval(-0.5, 0.5))
    assert a.start == np.arccos(0.5)
    assert a.end == np.arccos(-0.5)

    a = acos(interval(-1.5, 1.5))
    assert a.is_valid is None
    a = acos(interval(-2, -1.5))
    assert a.is_valid is False

    a = acos(interval(0, 2))
    assert a.is_valid is None

    a = acos(interval(2, 5))
    assert a.is_valid is False

    a = acos(0.5)
    assert a.start == np.arccos(0.5)
    assert a.end == np.arccos(0.5)

    a = acos(1.5)
    assert a.is_valid is False


def test_acos():
    assert acos(nan) is nan
    assert acos(zoo) is zoo

    assert acos.nargs == FiniteSet(1)
    assert acos(oo) == I*oo
    assert acos(-oo) == -I*oo

    # Note: acos(-x) = pi - acos(x)
    assert acos(0) == pi/2
    assert acos(S.Half) == pi/3
    assert acos(Rational(-1, 2)) == pi*Rational(2, 3)
    assert acos(1) == 0
    assert acos(-1) == pi
    assert acos(sqrt(2)/2) == pi/4
    assert acos(-sqrt(2)/2) == pi*Rational(3, 4)

    # check round-trip for exact values:
    for d in range(5, 13):
        for num in range(d):
            if gcd(num, d) == 1:
                assert acos(cos(num*pi/d)) == num*pi/d
                assert acos(-cos(num*pi/d)) == pi - num*pi/d
                assert acos(sin(num*pi/d)) == pi/2 - asin(sin(num*pi/d))
                assert acos(-sin(num*pi/d)) == pi/2 - asin(-sin(num*pi/d))

    assert acos(2*I) == pi/2 - asin(2*I)

    assert acos(x).diff(x) == -1/sqrt(1 - x**2)

    assert acos(0.2).is_real is True
    assert acos(-2).is_real is False
    assert acos(r).is_real is None

    assert acos(Rational(1, 7), evaluate=False).is_positive is True
    assert acos(Rational(-1, 7), evaluate=False).is_positive is True
    assert acos(Rational(3, 2), evaluate=False).is_positive is False
    assert acos(p).is_positive is None

    assert acos(2 + p).conjugate() != acos(10 + p)
    assert acos(-3 + n).conjugate() != acos(-3 + n)
    assert acos(Rational(1, 3)).conjugate() == acos(Rational(1, 3))
    assert acos(Rational(-1, 3)).conjugate() == acos(Rational(-1, 3))
    assert acos(p + n*I).conjugate() == acos(p - n*I)
    assert acos(z).conjugate() != acos(conjugate(z))

