
def test_SetKind_FiniteSet():
    assert FiniteSet(1, Matrix([1, 2])).kind is SetKind(UndefinedKind)
    assert FiniteSet(1, 2).kind is SetKind(NumberKind)

