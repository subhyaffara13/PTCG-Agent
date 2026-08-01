
def test_cosh_nonnegative():
    k = symbols('k', real=True)
    n = symbols('n', integer=True)

    assert cosh(k, evaluate=False).is_nonnegative is True
    assert cosh(k + 2*n*pi*I, evaluate=False).is_nonnegative is True
    assert cosh(I*pi/4, evaluate=False).is_nonnegative is True
    assert cosh(3*I*pi/4, evaluate=False).is_nonnegative is False
    assert cosh(S.Zero, evaluate=False).is_nonnegative is True

