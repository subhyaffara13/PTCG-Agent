
def test_Reals():
    assert 5 in S.Reals
    assert S.Pi in S.Reals
    assert -sqrt(2) in S.Reals
    assert (2, 5) not in S.Reals
    assert sqrt(-1) not in S.Reals
    assert S.Reals == Interval(-oo, oo)
    assert S.Reals != Interval(0, oo)
    assert S.Reals.is_subset(Interval(-oo, oo))
    assert S.Reals.intersect(Range(-oo, oo)) == Range(-oo, oo)
    assert S.ComplexInfinity not in S.Reals
    assert S.NaN not in S.Reals
    assert x + S.ComplexInfinity not in S.Reals


def test_Reals():
    sT(S.Reals, "Reals")

