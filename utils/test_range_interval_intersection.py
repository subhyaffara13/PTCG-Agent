
def test_range_interval_intersection():
    p = symbols('p', positive=True)
    assert isinstance(Range(3).intersect(Interval(p, p + 2)), Intersection)
    assert Range(4).intersect(Interval(0, 3)) == Range(4)
    assert Range(4).intersect(Interval(-oo, oo)) == Range(4)
    assert Range(4).intersect(Interval(1, oo)) == Range(1, 4)
    assert Range(4).intersect(Interval(1.1, oo)) == Range(2, 4)
    assert Range(4).intersect(Interval(0.1, 3)) == Range(1, 4)
    assert Range(4).intersect(Interval(0.1, 3.1)) == Range(1, 4)
    assert Range(4).intersect(Interval.open(0, 3)) == Range(1, 3)
    assert Range(4).intersect(Interval.open(0.1, 0.5)) is S.EmptySet
    assert Interval(-1, 5).intersect(S.Complexes) == Interval(-1, 5)
    assert Interval(-1, 5).intersect(S.Reals) == Interval(-1, 5)
    assert Interval(-1, 5).intersect(S.Integers) == Range(-1, 6)
    assert Interval(-1, 5).intersect(S.Naturals) == Range(1, 6)
    assert Interval(-1, 5).intersect(S.Naturals0) == Range(0, 6)

    # Null Range intersections
    assert Range(0).intersect(Interval(0.2, 0.8)) is S.EmptySet
    assert Range(0).intersect(Interval(-oo, oo)) is S.EmptySet

