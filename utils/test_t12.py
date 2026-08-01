
def test_T12():
    x, t = symbols('x t', real=True)
    # Does not evaluate the limit but returns an expression with erf
    assert limit(x * integrate(exp(-t**2), (t, 0, x))/(1 - exp(-x**2)),
                 x, 0) == 1

