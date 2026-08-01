
def test_Point2D():

    # Test Distance
    p1 = Point2D(1, 5)
    p2 = Point2D(4, 2.5)
    p3 = (6, 3)
    assert p1.distance(p2) == sqrt(61)/2
    assert p2.distance(p3) == sqrt(17)/2

    # Test coordinates
    assert p1.x == 1
    assert p1.y == 5
    assert p2.x == 4
    assert p2.y == S(5)/2
    assert p1.coordinates == (1, 5)
    assert p2.coordinates == (4, S(5)/2)

    # test bounds
    assert p1.bounds == (1, 5, 1, 5)

