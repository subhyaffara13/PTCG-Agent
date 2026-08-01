
def test_Mul_is_comparable():
    assert (x*y).is_comparable is False
    assert (x*2).is_comparable is False
    assert (sqrt(2)*Rational(1, 3)).is_comparable is True

