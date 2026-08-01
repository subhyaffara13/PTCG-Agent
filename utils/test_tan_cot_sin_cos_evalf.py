
def test_tan_cot_sin_cos_evalf():
    assert abs((tan(pi*Rational(8, 15))*cos(pi*Rational(8, 15))/sin(pi*Rational(8, 15)) - 1).evalf()) < 1e-14
    assert abs((cot(pi*Rational(4, 15))*sin(pi*Rational(4, 15))/cos(pi*Rational(4, 15)) - 1).evalf()) < 1e-14

