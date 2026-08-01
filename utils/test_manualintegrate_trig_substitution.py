
def test_manualintegrate_trig_substitution():
    assert manualintegrate(sqrt(16*x**2 - 9)/x, x) == \
        Piecewise((sqrt(16*x**2 - 9) - 3*acos(3/(4*x)),
                   And(x < Rational(3, 4), x > Rational(-3, 4))))
    assert manualintegrate(1/(x**4 * sqrt(25-x**2)), x) == \
        Piecewise((-sqrt(-x**2/25 + 1)/(125*x) -
                   (-x**2/25 + 1)**(3*S.Half)/(15*x**3), And(x < 5, x > -5)))
    assert manualintegrate(x**7/(49*x**2 + 1)**(3 * S.Half), x) == \
        ((49*x**2 + 1)**(5*S.Half)/28824005 -
         (49*x**2 + 1)**(3*S.Half)/5764801 +
         3*sqrt(49*x**2 + 1)/5764801 + 1/(5764801*sqrt(49*x**2 + 1)))

