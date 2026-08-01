
def test_derivs():
    x = Symbol('x')
    assert coth(x).diff(x) == -sinh(x)**(-2)
    assert sinh(x).diff(x) == cosh(x)
    assert cosh(x).diff(x) == sinh(x)
    assert tanh(x).diff(x) == -tanh(x)**2 + 1
    assert csch(x).diff(x) == -coth(x)*csch(x)
    assert sech(x).diff(x) == -tanh(x)*sech(x)
    assert acoth(x).diff(x) == 1/(-x**2 + 1)
    assert asinh(x).diff(x) == 1/sqrt(x**2 + 1)
    assert acosh(x).diff(x) == 1/(sqrt(x - 1)*sqrt(x + 1))
    assert acosh(x).diff(x) == acosh(x).rewrite(log).diff(x).together()
    assert atanh(x).diff(x) == 1/(-x**2 + 1)
    assert asech(x).diff(x) == -1/(x*sqrt(1 - x**2))
    assert acsch(x).diff(x) == -1/(x**2*sqrt(1 + x**(-2)))

