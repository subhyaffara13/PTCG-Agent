
def test_Complex():
    assert 5 in S.Complexes
    assert 5 + 4*I in S.Complexes
    assert S.Pi in S.Complexes
    assert -sqrt(2) in S.Complexes
    assert -I in S.Complexes
    assert sqrt(-1) in S.Complexes
    assert S.Complexes.intersect(S.Reals) == S.Reals
    assert S.Complexes.union(S.Reals) == S.Complexes
    assert S.Complexes == ComplexRegion(S.Reals*S.Reals)
    assert (S.Complexes == ComplexRegion(Interval(1, 2)*Interval(3, 4))) == False
    assert str(S.Complexes) == "Complexes"
    assert repr(S.Complexes) == "Complexes"

