
def test_integrate_derivatives():
    assert integrate(Derivative(f(x), x), x) == f(x)
    assert integrate(Derivative(f(y), y), x) == x*Derivative(f(y), y)
    assert integrate(Derivative(f(x), x)**2, x) == \
        Integral(Derivative(f(x), x)**2, x)

