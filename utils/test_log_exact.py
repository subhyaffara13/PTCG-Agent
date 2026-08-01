
def test_log_exact():
    # check for pi/2, pi/3, pi/4, pi/6, pi/8, pi/12; pi/5, pi/10:
    for n in range(-23, 24):
        if gcd(n, 24) != 1:
            assert log(exp(n*I*pi/24).rewrite(sqrt)) == n*I*pi/24
        for n in range(-9, 10):
            assert log(exp(n*I*pi/10).rewrite(sqrt)) == n*I*pi/10

    assert log(S.Half - I*sqrt(3)/2) == -I*pi/3
    assert log(Rational(-1, 2) + I*sqrt(3)/2) == I*pi*Rational(2, 3)
    assert log(-sqrt(2)/2 - I*sqrt(2)/2) == -I*pi*Rational(3, 4)
    assert log(-sqrt(3)/2 - I*S.Half) == -I*pi*Rational(5, 6)

    assert log(Rational(-1, 4) + sqrt(5)/4 - I*sqrt(sqrt(5)/8 + Rational(5, 8))) == -I*pi*Rational(2, 5)
    assert log(sqrt(Rational(5, 8) - sqrt(5)/8) + I*(Rational(1, 4) + sqrt(5)/4)) == I*pi*Rational(3, 10)
    assert log(-sqrt(sqrt(2)/4 + S.Half) + I*sqrt(S.Half - sqrt(2)/4)) == I*pi*Rational(7, 8)
    assert log(-sqrt(6)/4 - sqrt(2)/4 + I*(-sqrt(6)/4 + sqrt(2)/4)) == -I*pi*Rational(11, 12)

    assert log(-1 + I*sqrt(3)) == log(2) + I*pi*Rational(2, 3)
    assert log(5 + 5*I) == log(5*sqrt(2)) + I*pi/4
    assert log(sqrt(-12)) == log(2*sqrt(3)) + I*pi/2
    assert log(-sqrt(6) + sqrt(2) - I*sqrt(6) - I*sqrt(2)) == log(4) - I*pi*Rational(7, 12)
    assert log(-sqrt(6-3*sqrt(2)) - I*sqrt(6+3*sqrt(2))) == log(2*sqrt(3)) - I*pi*Rational(5, 8)
    assert log(1 + I*sqrt(2-sqrt(2))/sqrt(2+sqrt(2))) == log(2/sqrt(sqrt(2) + 2)) + I*pi/8
    assert log(cos(pi*Rational(7, 12)) + I*sin(pi*Rational(7, 12))) == I*pi*Rational(7, 12)
    assert log(cos(pi*Rational(6, 5)) + I*sin(pi*Rational(6, 5))) == I*pi*Rational(-4, 5)

    assert log(5*(1 + I)/sqrt(2)) == log(5) + I*pi/4
    assert log(sqrt(2)*(-sqrt(3) + 1 - sqrt(3)*I - I)) == log(4) - I*pi*Rational(7, 12)
    assert log(-sqrt(2)*(1 - I*sqrt(3))) == log(2*sqrt(2)) + I*pi*Rational(2, 3)
    assert log(sqrt(3)*I*(-sqrt(6 - 3*sqrt(2)) - I*sqrt(3*sqrt(2) + 6))) == log(6) - I*pi/8

    zero = (1 + sqrt(2))**2 - 3 - 2*sqrt(2)
    assert log(zero - I*sqrt(3)) == log(sqrt(3)) - I*pi/2
    assert unchanged(log, zero + I*zero) or log(zero + zero*I) is zoo

    # bail quickly if no obvious simplification is possible:
    assert unchanged(log, (sqrt(2)-1/sqrt(sqrt(3)+I))**1000)
    # beware of non-real coefficients
    assert unchanged(log, sqrt(2-sqrt(5))*(1 + I))

