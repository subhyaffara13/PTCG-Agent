
def test_W17():
    a, b = symbols('a b', positive=True)
    assert integrate(exp(-a*x)*besselj(0, b*x),
                 (x, 0, oo)) == 1/(b*sqrt(a**2/b**2 + 1))

