
def test_function_comparable():
    assert sin(x).is_comparable is False
    assert cos(x).is_comparable is False

    assert sin(Float('0.1')).is_comparable is True
    assert cos(Float('0.1')).is_comparable is True

    assert sin(E).is_comparable is True
    assert cos(E).is_comparable is True

    assert sin(Rational(1, 3)).is_comparable is True
    assert cos(Rational(1, 3)).is_comparable is True

