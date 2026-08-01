
def test_intersections():
    assert S.Integers.intersect(S.Reals) == S.Integers
    assert 5 in S.Integers.intersect(S.Reals)
    assert 5 in S.Integers.intersect(S.Reals)
    assert -5 not in S.Naturals.intersect(S.Reals)
    assert 5.5 not in S.Integers.intersect(S.Reals)
    assert 5 in S.Integers.intersect(Interval(3, oo))
    assert -5 in S.Integers.intersect(Interval(-oo, 3))
    assert all(x.is_Integer
            for x in take(10, S.Integers.intersect(Interval(3, oo)) ))

