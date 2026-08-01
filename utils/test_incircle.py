
def test_incircle():
    assert Triangle(Point(0, 0), Point(2, 0), Point(0, 2)).incircle \
        == Circle(Point(2 - sqrt(2), 2 - sqrt(2)), 2 - sqrt(2))

