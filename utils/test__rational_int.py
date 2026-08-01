
def test_Rational_int():
    assert int( Rational(7, 5)) == 1
    assert int( S.Half) == 0
    assert int(Rational(-1, 2)) == 0
    assert int(-Rational(7, 5)) == -1

