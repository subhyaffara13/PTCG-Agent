
def test_SetKind_EmptySet_UniversalSet():
    assert S.UniversalSet.kind is SetKind(UndefinedKind)
    assert EmptySet.kind is SetKind()

