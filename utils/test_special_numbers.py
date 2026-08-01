
def test_special_numbers():
    assert isinstance(S.NaN, Number) is True
    assert isinstance(S.Infinity, Number) is True
    assert isinstance(S.NegativeInfinity, Number) is True

    assert S.NaN.is_number is True
    assert S.Infinity.is_number is True
    assert S.NegativeInfinity.is_number is True
    assert S.ComplexInfinity.is_number is True

    assert isinstance(S.NaN, Rational) is False
    assert isinstance(S.Infinity, Rational) is False
    assert isinstance(S.NegativeInfinity, Rational) is False

    assert S.NaN.is_rational is not True
    assert S.Infinity.is_rational is not True
    assert S.NegativeInfinity.is_rational is not True

