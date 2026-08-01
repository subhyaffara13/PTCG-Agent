
def test_pretty_geometry():
    e = Segment((0, 1), (0, 2))
    assert pretty(e) == 'Segment2D(Point2D(0, 1), Point2D(0, 2))'
    e = Ray((1, 1), angle=4.02*pi)
    assert pretty(e) == 'Ray2D(Point2D(1, 1), Point2D(2, tan(pi/50) + 1))'

