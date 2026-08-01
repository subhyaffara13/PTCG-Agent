
def test_SetKind_DisjointUnion():
    A = FiniteSet(1, 2, 3)
    B = Interval(0, 5)
    assert DisjointUnion(A, B).kind is SetKind(NumberKind)

