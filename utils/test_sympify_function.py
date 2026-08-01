
def test_sympify_function():
    assert sympify('factor(x**2-1, x)') == -(1 - x)*(x + 1)
    assert sympify('sin(pi/2)*cos(pi)') == -Integer(1)

