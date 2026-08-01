
def test_issue_12598():
    r1 = Ray(Point(0, 1), Point(0.98, 0.79).n(2))
    r2 = Ray(Point(0, 0), Point(0.71, 0.71).n(2))
    assert str(r1.intersection(r2)[0]) == 'Point2D(0.82, 0.82)'
    l1 = Line((0, 0), (1, 1))
    l2 = Segment((-1, 1), (0, -1)).n(2)
    assert str(l1.intersection(l2)[0]) == 'Point2D(-0.33, -0.33)'
    l2 = Segment((-1, 1), (-1/2, 1/2)).n(2)
    assert not l1.intersection(l2)

