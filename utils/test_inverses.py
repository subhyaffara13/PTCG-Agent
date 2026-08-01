
def test_inverses():
    x = Symbol('x')
    assert sinh(x).inverse() == asinh
    raises(AttributeError, lambda: cosh(x).inverse())
    assert tanh(x).inverse() == atanh
    assert coth(x).inverse() == acoth
    assert asinh(x).inverse() == sinh
    assert acosh(x).inverse() == cosh
    assert atanh(x).inverse() == tanh
    assert acoth(x).inverse() == coth
    assert asech(x).inverse() == sech
    assert acsch(x).inverse() == csch


def test_inverses():
    raises(AttributeError, lambda: sin(x).inverse())
    raises(AttributeError, lambda: cos(x).inverse())
    assert tan(x).inverse() == atan
    assert cot(x).inverse() == acot
    raises(AttributeError, lambda: csc(x).inverse())
    raises(AttributeError, lambda: sec(x).inverse())
    assert asin(x).inverse() == sin
    assert acos(x).inverse() == cos
    assert atan(x).inverse() == tan
    assert acot(x).inverse() == cot

