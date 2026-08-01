
def test_intersection_symbolic_failing():
    n = Symbol('n', integer=True, positive=True)
    assert Intersection(Range(10, n), Range(4, 500, 5)) == Intersection(
        Range(14, n), Range(14, 500, 5))
    assert Intersection(Interval(10, n), Range(4, 500, 5)) == Intersection(
        Interval(14, n), Range(14, 500, 5))

