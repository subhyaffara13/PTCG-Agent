
def test_W23():
    a, b = symbols('a b', positive=True)
    r1 = integrate(integrate(x/(x**2 + y**2), (x, a, b)), (y, -oo, oo))
    assert r1.collect(pi).cancel() == -pi*a + pi*b

