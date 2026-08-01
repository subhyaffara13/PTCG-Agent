
def test_derivative_linearity():
    assert diff(-f(x), x) == -diff(f(x), x)
    assert diff(8*f(x), x) == 8*diff(f(x), x)
    assert diff(8*f(x), x) != 7*diff(f(x), x)
    assert diff(8*f(x)*x, x) == 8*f(x) + 8*x*diff(f(x), x)
    assert diff(8*f(x)*y*x, x).expand() == 8*y*f(x) + 8*y*x*diff(f(x), x)

