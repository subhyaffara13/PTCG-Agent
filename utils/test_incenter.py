
def test_incenter():
    assert Triangle(Point(0, 0), Point(1, 0), Point(0, 1)).incenter \
        == Point(1 - sqrt(2)/2, 1 - sqrt(2)/2)

