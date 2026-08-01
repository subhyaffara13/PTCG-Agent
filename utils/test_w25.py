
def test_W25():
    a, x, y = symbols('a x y', real=True)
    i1 = integrate(
        sin(a)*sin(y)/sqrt(1 - sin(a)**2*sin(x)**2*sin(y)**2),
        (x, 0, pi/2))
    i2 = integrate(i1, (y, 0, pi/2))
    assert (i2 - pi*a/2).simplify() == 0

