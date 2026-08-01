
def test_convex_hull():
    p = [Point(-5, -1), Point(-2, 1), Point(-2, -1), Point(-1, -3), \
         Point(0, 0), Point(1, 1), Point(2, 2), Point(2, -1), Point(3, 1), \
         Point(4, -1), Point(6, 2)]
    ch = Polygon(p[0], p[3], p[9], p[10], p[6], p[1])
    #test handling of duplicate points
    p.append(p[3])

    #more than 3 collinear points
    another_p = [Point(-45, -85), Point(-45, 85), Point(-45, 26), \
                 Point(-45, -24)]
    ch2 = Segment(another_p[0], another_p[1])

    assert convex_hull(*another_p) == ch2
    assert convex_hull(*p) == ch
    assert convex_hull(p[0]) == p[0]
    assert convex_hull(p[0], p[1]) == Segment(p[0], p[1])

    # no unique points
    assert convex_hull(*[p[-1]]*3) == p[-1]

    # collection of items
    assert convex_hull(*[Point(0, 0), \
                        Segment(Point(1, 0), Point(1, 1)), \
                        RegularPolygon(Point(2, 0), 2, 4)]) == \
        Polygon(Point(0, 0), Point(2, -2), Point(4, 0), Point(2, 2))


def test_convex_hull():
    raises(TypeError, lambda: convex_hull(Point(0, 0), 3))
    points = [(1, -1), (1, -2), (3, -1), (-5, -2), (15, -4)]
    assert convex_hull(*points, **{"polygon": False}) == (
        [Point2D(-5, -2), Point2D(1, -1), Point2D(3, -1), Point2D(15, -4)],
        [Point2D(-5, -2), Point2D(15, -4)])

