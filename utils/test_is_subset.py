
def test_is_subset():
    # covers line 101-102
    # initialize powerset(1), which is a subset of powerset(1,2)
    subset = PowerSet(FiniteSet(1))
    pset = PowerSet(FiniteSet(1, 2))
    bad_set = PowerSet(FiniteSet(2, 3))
    # assert "subset" is subset of pset == True
    assert subset.is_subset(pset)
    # assert "bad_set" is subset of pset == False
    assert not pset.is_subset(bad_set)


def test_is_subset():
    assert Interval(0, 1).is_subset(Interval(0, 2)) is True
    assert Interval(0, 3).is_subset(Interval(0, 2)) is False
    assert Interval(0, 1).is_subset(FiniteSet(0, 1)) is False

    assert FiniteSet(1, 2).is_subset(FiniteSet(1, 2, 3, 4))
    assert FiniteSet(4, 5).is_subset(FiniteSet(1, 2, 3, 4)) is False
    assert FiniteSet(1).is_subset(Interval(0, 2))
    assert FiniteSet(1, 2).is_subset(Interval(0, 2, True, True)) is False
    assert (Interval(1, 2) + FiniteSet(3)).is_subset(
        Interval(0, 2, False, True) + FiniteSet(2, 3))

    assert Interval(3, 4).is_subset(Union(Interval(0, 1), Interval(2, 5))) is True
    assert Interval(3, 6).is_subset(Union(Interval(0, 1), Interval(2, 5))) is False

    assert FiniteSet(1, 2, 3, 4).is_subset(Interval(0, 5)) is True
    assert S.EmptySet.is_subset(FiniteSet(1, 2, 3)) is True

    assert Interval(0, 1).is_subset(S.EmptySet) is False
    assert S.EmptySet.is_subset(S.EmptySet) is True

    raises(ValueError, lambda: S.EmptySet.is_subset(1))

    # tests for the issubset alias
    assert FiniteSet(1, 2, 3, 4).issubset(Interval(0, 5)) is True
    assert S.EmptySet.issubset(FiniteSet(1, 2, 3)) is True

    assert S.Naturals.is_subset(S.Integers)
    assert S.Naturals0.is_subset(S.Integers)

    assert FiniteSet(x).is_subset(FiniteSet(y)) is None
    assert FiniteSet(x).is_subset(FiniteSet(y).subs(y, x)) is True
    assert FiniteSet(x).is_subset(FiniteSet(y).subs(y, x+1)) is False

    assert Interval(0, 1).is_subset(Interval(0, 1, left_open=True)) is False
    assert Interval(-2, 3).is_subset(Union(Interval(-oo, -2), Interval(3, oo))) is False

    n = Symbol('n', integer=True)
    assert Range(-3, 4, 1).is_subset(FiniteSet(-10, 10)) is False
    assert Range(S(10)**100).is_subset(FiniteSet(0, 1, 2)) is False
    assert Range(6, 0, -2).is_subset(FiniteSet(2, 4, 6)) is True
    assert Range(1, oo).is_subset(FiniteSet(1, 2)) is False
    assert Range(-oo, 1).is_subset(FiniteSet(1)) is False
    assert Range(3).is_subset(FiniteSet(0, 1, n)) is None
    assert Range(n, n + 2).is_subset(FiniteSet(n, n + 1)) is True
    assert Range(5).is_subset(Interval(0, 4, right_open=True)) is False
    #issue 19513
    assert imageset(Lambda(n, 1/n), S.Integers).is_subset(S.Reals) is None

