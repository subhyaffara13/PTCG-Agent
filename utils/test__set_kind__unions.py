
def test_SetKind_Unions():
    assert Union(FiniteSet(Matrix([1, 2])), Interval(1, 2)).kind is SetKind(UndefinedKind)
    assert Union(Interval(1, 2), Interval(1, 7)).kind is SetKind(NumberKind)

