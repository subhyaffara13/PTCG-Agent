
def test_is_lambert():
    a, b, c = symbols('a,b,c')
    assert _is_lambert(x**2, x) is False
    assert _is_lambert(a**x**2+b*x+c, x) is True
    assert _is_lambert(E**2, x) is False
    assert _is_lambert(x*E**2, x) is False
    assert _is_lambert(3*log(x) - x*log(3), x) is True
    assert _is_lambert(log(log(x - 3)) + log(x-3), x) is True
    assert _is_lambert(5*x - 1 + 3*exp(2 - 7*x), x) is True
    assert _is_lambert((a/x + exp(x/2)).diff(x, 2), x) is True
    assert _is_lambert((x**2 - 2*x + 1).subs(x, (log(x) + 3*x)**2 - 1), x) is True
    assert _is_lambert(x*sinh(x) - 1, x) is True
    assert _is_lambert(x*cos(x) - 5, x) is True
    assert _is_lambert(tanh(x) - 5*x, x) is True
    assert _is_lambert(cosh(x) - sinh(x), x) is False

