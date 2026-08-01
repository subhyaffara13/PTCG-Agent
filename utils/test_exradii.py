
def test_exradii():
    t = Triangle(Point(0, 0), Point(6, 0), Point(0, 2))
    assert t.exradii[t.sides[2]] == (-2 + sqrt(10))

