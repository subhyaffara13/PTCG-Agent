
def test_union_RealSubSet():
    assert (S.Complexes).union(Interval(1, 2)) == S.Complexes
    assert (S.Complexes).union(S.Integers) == S.Complexes

