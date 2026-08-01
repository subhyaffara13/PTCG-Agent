
def test_W7():
    a = symbols('a', positive=True)
    r1 = integrate(cos(x)/(x**2 + a**2), (x, -oo, oo))
    assert r1.simplify() == pi*exp(-a)/a

