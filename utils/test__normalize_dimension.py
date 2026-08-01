
def test__normalize_dimension():
    assert Point._normalize_dimension(Point(1, 2), Point(3, 4)) == [
        Point(1, 2), Point(3, 4)]
    assert Point._normalize_dimension(
        Point(1, 2), Point(3, 4, 0), on_morph='ignore') == [
        Point(1, 2, 0), Point(3, 4, 0)]

