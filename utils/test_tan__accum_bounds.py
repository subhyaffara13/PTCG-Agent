
def test_tan_AccumBounds():
    assert tan(AccumBounds(-oo, oo)) == AccumBounds(-oo, oo)
    assert tan(AccumBounds(S.Pi/3, S.Pi*Rational(2, 3))) == AccumBounds(-oo, oo)
    assert tan(AccumBounds(S.Pi/6, S.Pi/3)) == AccumBounds(tan(S.Pi/6), tan(S.Pi/3))

