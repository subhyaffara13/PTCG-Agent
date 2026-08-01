
def test_asec():
    z = Symbol('z', zero=True)
    assert asec(z) is zoo
    assert asec(nan) is nan
    assert asec(1) == 0
    assert asec(-1) == pi
    assert asec(oo) == pi/2
    assert asec(-oo) == pi/2
    assert asec(zoo) == pi/2

    assert asec(sec(pi*Rational(13, 4))) == pi*Rational(3, 4)
    assert asec(1 + sqrt(5)) == pi*Rational(2, 5)
    assert asec(2/sqrt(3)) == pi/6
    assert asec(sqrt(4 - 2*sqrt(2))) == pi/8
    assert asec(-sqrt(4 + 2*sqrt(2))) == pi*Rational(5, 8)
    assert asec(sqrt(2 + 2*sqrt(5)/5)) == pi*Rational(3, 10)
    assert asec(-sqrt(2 + 2*sqrt(5)/5)) == pi*Rational(7, 10)
    assert asec(sqrt(2) - sqrt(6)) == pi*Rational(11, 12)

    for d in [3, 4, 6]:
        for num in range(d):
            if gcd(num, d) == 1:
                assert asec(sec(num*pi/d)) == num*pi/d
                assert asec(-sec(num*pi/d)) == pi - num*pi/d
                assert asec(csc(num*pi/d)) == pi/2 - acsc(csc(num*pi/d))
                assert asec(-csc(num*pi/d)) == pi/2 - acsc(-csc(num*pi/d))

    assert asec(x).diff(x) == 1/(x**2*sqrt(1 - 1/x**2))

    assert asec(x).rewrite(log) == I*log(sqrt(1 - 1/x**2) + I/x) + pi/2
    assert asec(x).rewrite(asin) == -asin(1/x) + pi/2
    assert asec(x).rewrite(acos) == acos(1/x)
    assert asec(x).rewrite(atan) == \
        pi*(1 - sqrt(x**2)/x)/2 + sqrt(x**2)*atan(sqrt(x**2 - 1))/x
    assert asec(x).rewrite(acot) == \
        pi*(1 - sqrt(x**2)/x)/2 + sqrt(x**2)*acot(1/sqrt(x**2 - 1))/x
    assert asec(x).rewrite(acsc) == -acsc(x) + pi/2
    raises(ArgumentIndexError, lambda: asec(x).fdiff(2))

