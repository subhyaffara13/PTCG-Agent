
def test_U6():
    h = Function('h')
    T = integrate(f(y), (y, h(x), g(x)))
    assert T.diff(x) == (
        f(g(x))*Derivative(g(x), x) - f(h(x))*Derivative(h(x), x))

