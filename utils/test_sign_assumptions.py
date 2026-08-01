
def test_sign_assumptions():
    p = Symbol('p', positive=True)
    n = Symbol('n', negative=True)
    assert sinh(n).is_negative is True
    assert sinh(p).is_positive is True
    assert cosh(n).is_positive is True
    assert cosh(p).is_positive is True
    assert tanh(n).is_negative is True
    assert tanh(p).is_positive is True
    assert csch(n).is_negative is True
    assert csch(p).is_positive is True
    assert sech(n).is_positive is True
    assert sech(p).is_positive is True
    assert coth(n).is_negative is True
    assert coth(p).is_positive is True

