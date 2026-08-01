
def test_Add_is_positive_2():
    e = Rational(1, 3) - sqrt(8)
    assert e.is_positive is False
    assert e.is_negative is True

    e = pi - 1
    assert e.is_positive is True
    assert e.is_negative is False

