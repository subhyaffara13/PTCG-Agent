
def test_V15():
    r1 = integrate(x*acot(x/y), x)
    assert simplify(r1 - (x*y + (x**2 + y**2)*acot(x/y))/2) == 0

