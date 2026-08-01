
def test_medial():
    assert Triangle(Point(0, 0), Point(1, 0), Point(0, 1)).medial \
        == Triangle(Point(S.Half, 0), Point(S.Half, S.Half), Point(0, S.Half))

