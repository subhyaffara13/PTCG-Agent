
def test_sin_AccumBounds():
    assert sin(AccumBounds(-oo, oo)) == AccumBounds(-1, 1)
    assert sin(AccumBounds(0, oo)) == AccumBounds(-1, 1)
    assert sin(AccumBounds(-oo, 0)) == AccumBounds(-1, 1)
    assert sin(AccumBounds(0, 2*S.Pi)) == AccumBounds(-1, 1)
    assert sin(AccumBounds(0, S.Pi*Rational(3, 4))) == AccumBounds(0, 1)
    assert sin(AccumBounds(S.Pi*Rational(3, 4), S.Pi*Rational(7, 4))) == AccumBounds(-1, sin(S.Pi*Rational(3, 4)))
    assert sin(AccumBounds(S.Pi/4, S.Pi/3)) == AccumBounds(sin(S.Pi/4), sin(S.Pi/3))
    assert sin(AccumBounds(S.Pi*Rational(3, 4), S.Pi*Rational(5, 6))) == AccumBounds(sin(S.Pi*Rational(5, 6)), sin(S.Pi*Rational(3, 4)))

