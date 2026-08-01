
def test_range_range_intersection():
    for a, b, r in [
            (Range(0), Range(1), S.EmptySet),
            (Range(3), Range(4, oo), S.EmptySet),
            (Range(3), Range(-3, -1), S.EmptySet),
            (Range(1, 3), Range(0, 3), Range(1, 3)),
            (Range(1, 3), Range(1, 4), Range(1, 3)),
            (Range(1, oo, 2), Range(2, oo, 2), S.EmptySet),
            (Range(0, oo, 2), Range(oo), Range(0, oo, 2)),
            (Range(0, oo, 2), Range(100), Range(0, 100, 2)),
            (Range(2, oo, 2), Range(oo), Range(2, oo, 2)),
            (Range(0, oo, 2), Range(5, 6), S.EmptySet),
            (Range(2, 80, 1), Range(55, 71, 4), Range(55, 71, 4)),
            (Range(0, 6, 3), Range(-oo, 5, 3), S.EmptySet),
            (Range(0, oo, 2), Range(5, oo, 3), Range(8, oo, 6)),
            (Range(4, 6, 2), Range(2, 16, 7), S.EmptySet),]:
        assert a.intersect(b) == r
        assert a.intersect(b.reversed) == r
        assert a.reversed.intersect(b) == r
        assert a.reversed.intersect(b.reversed) == r
        a, b = b, a
        assert a.intersect(b) == r
        assert a.intersect(b.reversed) == r
        assert a.reversed.intersect(b) == r
        assert a.reversed.intersect(b.reversed) == r

