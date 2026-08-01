
def test_intersection_symbolic():
    n = Symbol('n')
    # These should not throw an error
    assert isinstance(Intersection(Range(n), Range(100)), Intersection)
    assert isinstance(Intersection(Range(n), Interval(1, 100)), Intersection)
    assert isinstance(Intersection(Range(100), Interval(1, n)), Intersection)

