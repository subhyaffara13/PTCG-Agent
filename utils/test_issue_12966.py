
def test_issue_12966():
    poly = Polygon(Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 5),
        Point(10, 5), Point(10, 0))
    t = Symbol('t')
    pt = poly.arbitrary_point(t)
    DELTA = 5/poly.perimeter
    assert [pt.subs(t, DELTA*i) for i in range(int(1/DELTA))] == [
        Point(0, 0), Point(0, 5), Point(0, 10), Point(5, 10),
        Point(5, 5), Point(10, 5), Point(10, 0), Point(5, 0)]

