
def test_smallest_angle():
    a = Line(Point(1, 1), Point(1, 2))
    b = Line(Point(1, 1),Point(2, 3))
    assert a.smallest_angle_between(b) == acos(2*sqrt(5)/5)

