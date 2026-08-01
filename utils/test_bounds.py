
def test_bounds():
    e1 = Ellipse(Point(0, 0), 3, 5)
    e2 = Ellipse(Point(2, -2), 7, 7)
    c1 = Circle(Point(2, -2), 7)
    c2 = Circle(Point(-2, 0), Point(0, 2), Point(2, 0))
    assert e1.bounds == (-3, -5, 3, 5)
    assert e2.bounds == (-5, -9, 9, 5)
    assert c1.bounds == (-5, -9, 9, 5)
    assert c2.bounds == (-2, -2, 2, 2)

