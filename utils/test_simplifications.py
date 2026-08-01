
def test_simplifications():
    x = Symbol('x')
    assert sinh(asinh(x)) == x
    assert sinh(acosh(x)) == sqrt(x - 1) * sqrt(x + 1)
    assert sinh(atanh(x)) == x/sqrt(1 - x**2)
    assert sinh(acoth(x)) == 1/(sqrt(x - 1) * sqrt(x + 1))

    assert cosh(asinh(x)) == sqrt(1 + x**2)
    assert cosh(acosh(x)) == x
    assert cosh(atanh(x)) == 1/sqrt(1 - x**2)
    assert cosh(acoth(x)) == x/(sqrt(x - 1) * sqrt(x + 1))

    assert tanh(asinh(x)) == x/sqrt(1 + x**2)
    assert tanh(acosh(x)) == sqrt(x - 1) * sqrt(x + 1) / x
    assert tanh(atanh(x)) == x
    assert tanh(acoth(x)) == 1/x

    assert coth(asinh(x)) == sqrt(1 + x**2)/x
    assert coth(acosh(x)) == x/(sqrt(x - 1) * sqrt(x + 1))
    assert coth(atanh(x)) == 1/x
    assert coth(acoth(x)) == x

    assert csch(asinh(x)) == 1/x
    assert csch(acosh(x)) == 1/(sqrt(x - 1) * sqrt(x + 1))
    assert csch(atanh(x)) == sqrt(1 - x**2)/x
    assert csch(acoth(x)) == sqrt(x - 1) * sqrt(x + 1)

    assert sech(asinh(x)) == 1/sqrt(1 + x**2)
    assert sech(acosh(x)) == 1/x
    assert sech(atanh(x)) == sqrt(1 - x**2)
    assert sech(acoth(x)) == sqrt(x - 1) * sqrt(x + 1)/x

