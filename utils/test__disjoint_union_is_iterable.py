
def test_DisjointUnion_is_iterable():
    assert DisjointUnion(S.Integers, S.Naturals, S.Rationals).is_iterable is True
    assert DisjointUnion(S.EmptySet, S.Reals).is_iterable is False
    assert DisjointUnion(FiniteSet(1, 2, 3), S.EmptySet, FiniteSet(x, y)).is_iterable is True
    assert DisjointUnion(S.EmptySet, S.EmptySet).is_iterable is False

