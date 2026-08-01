
def test_tan_cot_sin_cos_ratsimp():
    assert 1 == (tan(pi*Rational(8, 15))*cos(pi*Rational(8, 15))/sin(pi*Rational(8, 15))).ratsimp()
    assert 1 == (cot(pi*Rational(4, 15))*sin(pi*Rational(4, 15))/cos(pi*Rational(4, 15))).ratsimp()

