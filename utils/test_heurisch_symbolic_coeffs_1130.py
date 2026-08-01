
def test_heurisch_symbolic_coeffs_1130():
    y = Symbol('y')
    assert heurisch_wrapper(1/(x**2 + y), x) == Piecewise(
    (log(x - sqrt(-y))/(2*sqrt(-y)) - log(x + sqrt(-y))/(2*sqrt(-y)),
    Ne(y, 0)), (-1/x, True))
    y = Symbol('y', positive=True)
    assert heurisch_wrapper(1/(x**2 + y), x) == (atan(x/sqrt(y))/sqrt(y))

