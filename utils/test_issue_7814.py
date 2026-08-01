
def test_issue_7814():
    circle = Circle(Point(x, 0), y)
    line = Line(Point(k, z), slope=0)
    _s = sqrt((y - z)*(y + z))
    assert line.intersection(circle) == [Point2D(x + _s, z), Point2D(x - _s, z)]

