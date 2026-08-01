
def test_issue_11730():
    unit = Interval(0, 1)
    square = ComplexRegion(unit ** 2)

    assert Union(S.Complexes, FiniteSet(oo)) != S.Complexes
    assert Union(S.Complexes, FiniteSet(eye(4))) != S.Complexes
    assert Union(unit, square) == square
    assert Intersection(S.Reals, square) == unit

