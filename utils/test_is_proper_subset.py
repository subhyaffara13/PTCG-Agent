
def test_is_proper_subset():
    assert Interval(0, 1).is_proper_subset(Interval(0, 2)) is True
    assert Interval(0, 3).is_proper_subset(Interval(0, 2)) is False
    assert S.EmptySet.is_proper_subset(FiniteSet(1, 2, 3)) is True

    raises(ValueError, lambda: Interval(0, 1).is_proper_subset(0))

