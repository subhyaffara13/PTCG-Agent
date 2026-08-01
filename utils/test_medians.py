
def test_medians():
    t = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    assert t.medians[Point(0, 0)] == Segment(Point(0, 0), Point(S.Half, S.Half))

