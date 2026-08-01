
def test_V1():
    x = symbols('x', real=True)
    assert integrate(abs(x), x) == Piecewise((-x**2/2, x <= 0), (x**2/2, True))

