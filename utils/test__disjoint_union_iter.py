
def test_DisjointUnion_iter():
    D = DisjointUnion(FiniteSet(3, 5, 7, 9), FiniteSet(x, y, z))
    it = iter(D)
    L1 = [(x, 1), (y, 1), (z, 1)]
    L2 = [(3, 0), (5, 0), (7, 0), (9, 0)]
    nxt = next(it)
    assert nxt in L2
    L2.remove(nxt)
    nxt = next(it)
    assert nxt in L1
    L1.remove(nxt)
    nxt = next(it)
    assert nxt in L2
    L2.remove(nxt)
    nxt = next(it)
    assert nxt in L1
    L1.remove(nxt)
    nxt = next(it)
    assert nxt in L2
    L2.remove(nxt)
    nxt = next(it)
    assert nxt in L1
    L1.remove(nxt)
    nxt = next(it)
    assert nxt in L2
    L2.remove(nxt)
    raises(StopIteration, lambda: next(it))

    raises(ValueError, lambda: iter(DisjointUnion(Interval(0, 1), S.EmptySet)))

