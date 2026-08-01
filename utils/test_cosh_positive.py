
def test_cosh_positive():
    # See issue 11721
    # cosh(x) is positive for real values of x
    k = symbols('k', real=True)
    n = symbols('n', integer=True)

    assert cosh(k, evaluate=False).is_positive is True
    assert cosh(k + 2*n*pi*I, evaluate=False).is_positive is True
    assert cosh(I*pi/4, evaluate=False).is_positive is True
    assert cosh(3*I*pi/4, evaluate=False).is_positive is False

