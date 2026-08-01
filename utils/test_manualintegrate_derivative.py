
def test_manualintegrate_derivative():
    assert manualintegrate(pi * Derivative(x**2 + 2*x + 3), x) == \
        pi * (x**2 + 2*x + 3)
    assert manualintegrate(Derivative(x**2 + 2*x + 3, y), x) == \
        Integral(Derivative(x**2 + 2*x + 3, y))
    assert manualintegrate(Derivative(sin(x), x, x, x, y), x) == \
        Derivative(sin(x), x, x, y)

