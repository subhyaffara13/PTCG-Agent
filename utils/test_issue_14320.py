
def test_issue_14320():
    assert asin(sin(2)) == -2 + pi and (-pi/2 <= -2 + pi <= pi/2) and sin(2) == sin(-2 + pi)
    assert asin(cos(2)) == -2 + pi/2 and (-pi/2 <= -2 + pi/2 <= pi/2) and cos(2) == sin(-2 + pi/2)
    assert acos(sin(2)) == -pi/2 + 2 and (0 <= -pi/2 + 2 <= pi) and sin(2) == cos(-pi/2 + 2)
    assert acos(cos(20)) == -6*pi + 20 and (0 <= -6*pi + 20 <= pi) and cos(20) == cos(-6*pi + 20)
    assert acos(cos(30)) == -30 + 10*pi and (0 <= -30 + 10*pi <= pi) and cos(30) == cos(-30 + 10*pi)

    assert atan(tan(17)) == -5*pi + 17 and (-pi/2 < -5*pi + 17 < pi/2) and tan(17) == tan(-5*pi + 17)
    assert atan(tan(15)) == -5*pi + 15 and (-pi/2 < -5*pi + 15 < pi/2) and tan(15) == tan(-5*pi + 15)
    assert atan(cot(12)) == -12 + pi*Rational(7, 2) and (-pi/2 < -12 + pi*Rational(7, 2) < pi/2) and cot(12) == tan(-12 + pi*Rational(7, 2))
    assert acot(cot(15)) == -5*pi + 15 and (-pi/2 < -5*pi + 15 <= pi/2) and cot(15) == cot(-5*pi + 15)
    assert acot(tan(19)) == -19 + pi*Rational(13, 2) and (-pi/2 < -19 + pi*Rational(13, 2) <= pi/2) and tan(19) == cot(-19 + pi*Rational(13, 2))

    assert asec(sec(11)) == -11 + 4*pi and (0 <= -11 + 4*pi <= pi) and cos(11) == cos(-11 + 4*pi)
    assert asec(csc(13)) == -13 + pi*Rational(9, 2) and (0 <= -13 + pi*Rational(9, 2) <= pi) and sin(13) == cos(-13 + pi*Rational(9, 2))
    assert acsc(csc(14)) == -4*pi + 14 and (-pi/2 <= -4*pi + 14 <= pi/2) and sin(14) == sin(-4*pi + 14)
    assert acsc(sec(10)) == pi*Rational(-7, 2) + 10 and (-pi/2 <= pi*Rational(-7, 2) + 10 <= pi/2) and cos(10) == sin(pi*Rational(-7, 2) + 10)

