
def test_DisjointUnion_len():
    assert len(DisjointUnion(FiniteSet(3, 5, 7, 9), FiniteSet(x, y, z))) == 7
    assert len(DisjointUnion(S.EmptySet, S.EmptySet, FiniteSet(x, y, z), S.EmptySet)) == 3
    raises(ValueError, lambda: len(DisjointUnion(Interval(0, 1), S.EmptySet)))

