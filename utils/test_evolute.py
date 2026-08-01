
def test_evolute():
    #ellipse centered at h,k
    x, y, h, k = symbols('x y h k',real = True)
    a, b = symbols('a b')
    e = Ellipse(Point(h, k), a, b)
    t1 = (e.hradius*(x - e.center.x))**Rational(2, 3)
    t2 = (e.vradius*(y - e.center.y))**Rational(2, 3)
    E = t1 + t2 - (e.hradius**2 - e.vradius**2)**Rational(2, 3)
    assert e.evolute() == E
    #Numerical Example
    e = Ellipse(Point(1, 1), 6, 3)
    t1 = (6*(x - 1))**Rational(2, 3)
    t2 = (3*(y - 1))**Rational(2, 3)
    E = t1 + t2 - (27)**Rational(2, 3)
    assert e.evolute() == E

