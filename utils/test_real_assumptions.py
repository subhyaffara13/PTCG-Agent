
def test_real_assumptions():
    z = Symbol('z', real=False)
    assert sinh(z).is_real is None
    assert cosh(z).is_real is None
    assert tanh(z).is_real is None
    assert sech(z).is_real is None
    assert csch(z).is_real is None
    assert coth(z).is_real is None


def test_real_assumptions():
    z = Symbol('z', real=False, finite=True)
    assert sin(z).is_real is None
    assert cos(z).is_real is None
    assert tan(z).is_real is False
    assert sec(z).is_real is None
    assert csc(z).is_real is None
    assert cot(z).is_real is False
    assert asin(p).is_real is None
    assert asin(n).is_real is None
    assert asec(p).is_real is None
    assert asec(n).is_real is None
    assert acos(p).is_real is None
    assert acos(n).is_real is None
    assert acsc(p).is_real is None
    assert acsc(n).is_real is None
    assert atan(p).is_positive is True
    assert atan(n).is_negative is True
    assert acot(p).is_positive is True
    assert acot(n).is_negative is True

