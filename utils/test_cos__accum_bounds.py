
def test_cos_AccumBounds():
    assert cos(AccumBounds(-oo, oo)) == AccumBounds(-1, 1)
    assert cos(AccumBounds(0, oo)) == AccumBounds(-1, 1)
    assert cos(AccumBounds(-oo, 0)) == AccumBounds(-1, 1)
    assert cos(AccumBounds(0, 2*S.Pi)) == AccumBounds(-1, 1)
    assert cos(AccumBounds(-S.Pi/3, S.Pi/4)) == AccumBounds(cos(-S.Pi/3), 1)
    assert cos(AccumBounds(S.Pi*Rational(3, 4), S.Pi*Rational(5, 4))) == AccumBounds(-1, cos(S.Pi*Rational(3, 4)))
    assert cos(AccumBounds(S.Pi*Rational(5, 4), S.Pi*Rational(4, 3))) == AccumBounds(cos(S.Pi*Rational(5, 4)), cos(S.Pi*Rational(4, 3)))
    assert cos(AccumBounds(S.Pi/4, S.Pi/3)) == AccumBounds(cos(S.Pi/3), cos(S.Pi/4))

