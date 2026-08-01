
def test_is_convex():
    assert is_convex(1/x, x, domain=Interval.open(0, oo)) == True
    assert is_convex(1/x, x, domain=Interval(-oo, 0)) == False
    assert is_convex(x**2, x, domain=Interval(0, oo)) == True
    assert is_convex(1/x**3, x, domain=Interval.Lopen(0, oo)) == True
    assert is_convex(-1/x**3, x, domain=Interval.Ropen(-oo, 0)) == True
    assert is_convex(log(x) ,x) == False
    assert is_convex(x**2+y**2, x, y) == True
    assert is_convex(cos(x) + cos(y), x) == False
    assert is_convex(8*x**2 - 2*y**2, x, y) == False

