
def test_viete():
    r1, r2 = symbols('r1, r2')

    assert viete(
        a*x**2 + b*x + c, [r1, r2], x) == [(r1 + r2, -b/a), (r1*r2, c/a)]

    raises(ValueError, lambda: viete(1, [], x))
    raises(ValueError, lambda: viete(x**2 + 1, [r1]))

    raises(MultivariatePolynomialError, lambda: viete(x + y, [r1]))

