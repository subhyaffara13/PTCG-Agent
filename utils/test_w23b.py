
def test_W23b():
    # like W23 but limits are reversed
    a, b = symbols('a b', positive=True)
    r2 = integrate(integrate(x/(x**2 + y**2), (y, -oo, oo)), (x, a, b))
    assert r2.collect(pi) == pi*(-a + b)

