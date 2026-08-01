
def test_issue_4311_fast():
    x = symbols('x', real=True)
    assert integrate(x*abs(9-x**2), x) == Piecewise(
        (x**4/4 - 9*x**2/2, x <= -3),
        (-x**4/4 + 9*x**2/2 - Rational(81, 2), x <= 3),
        (x**4/4 - 9*x**2/2, True))

