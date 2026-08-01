
def test_asin():
    R, x, y = ring('x, y', QQ)
    assert rs_asin(x + x*y, x, 5) == x**3*y**3/6 + x**3*y**2/2 + x**3*y/2 + \
        x**3/6 + x*y + x
    assert rs_asin(x*y + x**2*y**3, x, 6) == x**5*y**7/2 + 3*x**5*y**5/40 + \
        x**4*y**5/2 + x**3*y**3/6 + x**2*y**3 + x*y


def test_asin():
    a = asin(interval(-0.5, 0.5))
    assert a.start == np.arcsin(-0.5)
    assert a.end == np.arcsin(0.5)

    a = asin(interval(-1.5, 1.5))
    assert a.is_valid is None
    a = asin(interval(-2, -1.5))
    assert a.is_valid is False

    a = asin(interval(0, 2))
    assert a.is_valid is None

    a = asin(interval(2, 5))
    assert a.is_valid is False

    a = asin(0.5)
    assert a.start == np.arcsin(0.5)
    assert a.end == np.arcsin(0.5)

    a = asin(1.5)
    assert a.is_valid is False


def test_asin():
    assert asin(nan) is nan

    assert asin.nargs == FiniteSet(1)
    assert asin(oo) == -I*oo
    assert asin(-oo) == I*oo
    assert asin(zoo) is zoo

    # Note: asin(-x) = - asin(x)
    assert asin(0) == 0
    assert asin(1) == pi/2
    assert asin(-1) == -pi/2
    assert asin(sqrt(3)/2) == pi/3
    assert asin(-sqrt(3)/2) == -pi/3
    assert asin(sqrt(2)/2) == pi/4
    assert asin(-sqrt(2)/2) == -pi/4
    assert asin(sqrt((5 - sqrt(5))/8)) == pi/5
    assert asin(-sqrt((5 - sqrt(5))/8)) == -pi/5
    assert asin(S.Half) == pi/6
    assert asin(Rational(-1, 2)) == -pi/6
    assert asin((sqrt(2 - sqrt(2)))/2) == pi/8
    assert asin(-(sqrt(2 - sqrt(2)))/2) == -pi/8
    assert asin((sqrt(5) - 1)/4) == pi/10
    assert asin(-(sqrt(5) - 1)/4) == -pi/10
    assert asin((sqrt(3) - 1)/sqrt(2**3)) == pi/12
    assert asin(-(sqrt(3) - 1)/sqrt(2**3)) == -pi/12

    # check round-trip for exact values:
    for d in [5, 6, 8, 10, 12]:
        for n in range(-(d//2), d//2 + 1):
            if gcd(n, d) == 1:
                assert asin(sin(n*pi/d)) == n*pi/d

    assert asin(x).diff(x) == 1/sqrt(1 - x**2)

    assert asin(0.2, evaluate=False).is_real is True
    assert asin(-2).is_real is False
    assert asin(r).is_real is None

    assert asin(-2*I) == -I*asinh(2)

    assert asin(Rational(1, 7), evaluate=False).is_positive is True
    assert asin(Rational(-1, 7), evaluate=False).is_positive is False
    assert asin(p).is_positive is None
    assert asin(sin(Rational(7, 2))) == Rational(-7, 2) + pi
    assert asin(sin(Rational(-7, 4))) == Rational(7, 4) - pi
    assert unchanged(asin, cos(x))

