
def test_EmptySet():
    assert S.EmptySet.as_relational(Symbol('x')) is S.false
    assert S.EmptySet.intersect(S.UniversalSet) == S.EmptySet
    assert S.EmptySet.boundary == S.EmptySet

