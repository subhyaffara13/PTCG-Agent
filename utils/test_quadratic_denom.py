
def test_quadratic_denom():
    f = (5*x + 2)/(3*x**2 - 2*x + 8)
    assert manualintegrate(f, x) == 5*log(3*x**2 - 2*x + 8)/6 + 11*sqrt(23)*atan(3*sqrt(23)*(x - Rational(1, 3))/23)/69
    g = 3/(2*x**2 + 3*x + 1)
    assert manualintegrate(g, x) == 3*log(4*x + 2) - 3*log(4*x + 4)

