
def test_is_finiteset():
    for s in [S.Naturals, S.Naturals0, S.Integers, S.Rationals, S.Reals,
            S.UniversalSet]:
        assert s.is_finite_set is False

    assert S.EmptySet.is_finite_set is True

    assert FiniteSet(1, 2).is_finite_set is True
    assert Interval(1, 2).is_finite_set is False
    assert Interval(x, y).is_finite_set is None
    assert ProductSet(FiniteSet(1), FiniteSet(2)).is_finite_set is True
    assert ProductSet(FiniteSet(1), Interval(1, 2)).is_finite_set is False
    assert ProductSet(FiniteSet(1), Interval(x, y)).is_finite_set is None
    assert Union(Interval(0, 1), Interval(2, 3)).is_finite_set is False
    assert Union(FiniteSet(1), Interval(2, 3)).is_finite_set is False
    assert Union(FiniteSet(1), FiniteSet(2)).is_finite_set is True
    assert Union(FiniteSet(1), Interval(x, y)).is_finite_set is None
    assert Intersection(Interval(x, y), FiniteSet(1)).is_finite_set is True
    assert Intersection(Interval(x, y), Interval(1, 2)).is_finite_set is None
    assert Intersection(FiniteSet(x), FiniteSet(y)).is_finite_set is True
    assert Complement(FiniteSet(1), Interval(x, y)).is_finite_set is True
    assert Complement(Interval(x, y), FiniteSet(1)).is_finite_set is None
    assert Complement(Interval(1, 2), FiniteSet(x)).is_finite_set is False
    assert DisjointUnion(Interval(-5, 3), FiniteSet(x, y)).is_finite_set is False
    assert DisjointUnion(S.EmptySet, FiniteSet(x, y), S.EmptySet).is_finite_set is True

