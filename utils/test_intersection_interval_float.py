
def test_intersection_interval_float():
    # intersection of Intervals with mixed Rational/Float boundaries should
    # lead to Float boundaries in all cases regardless of which Interval is
    # open or closed.
    typs = [
        (Interval, Interval, Interval),
        (Interval, Interval.open, Interval.open),
        (Interval, Interval.Lopen, Interval.Lopen),
        (Interval, Interval.Ropen, Interval.Ropen),
        (Interval.open, Interval.open, Interval.open),
        (Interval.open, Interval.Lopen, Interval.open),
        (Interval.open, Interval.Ropen, Interval.open),
        (Interval.Lopen, Interval.Lopen, Interval.Lopen),
        (Interval.Lopen, Interval.Ropen, Interval.open),
        (Interval.Ropen, Interval.Ropen, Interval.Ropen),
    ]

    as_float = lambda a1, a2: a2 if isinstance(a2, float) else a1

    for t1, t2, t3 in typs:
        for t1i, t2i in [(t1, t2), (t2, t1)]:
            for a1, a2, b1, b2 in cartes([2, 2.0], [2, 2.0], [3, 3.0], [3, 3.0]):
                I1 = t1(a1, b1)
                I2 = t2(a2, b2)
                I3 = t3(as_float(a1, a2), as_float(b1, b2))
                assert I1.intersect(I2) == I3

