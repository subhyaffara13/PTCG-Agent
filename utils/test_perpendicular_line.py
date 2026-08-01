
def test_perpendicular_line():
    # 3d - requires a particular orthogonal to be selected
    p1, p2, p3 = Point(0, 0, 0), Point(2, 3, 4), Point(-2, 2, 0)
    l = Line(p1, p2)
    p = l.perpendicular_line(p3)
    assert p.p1 == p3
    assert p.p2 in l
    # 2d - does not require special selection
    p1, p2, p3 = Point(0, 0), Point(2, 3), Point(-2, 2)
    l = Line(p1, p2)
    p = l.perpendicular_line(p3)
    assert p.p1 == p3
    # p is directed from l to p3
    assert p.direction.unit == (p3 - l.projection(p3)).unit

