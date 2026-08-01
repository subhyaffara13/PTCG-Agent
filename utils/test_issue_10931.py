
def test_issue_10931():
    assert S.Integers - S.Integers == EmptySet
    assert S.Integers - S.Reals == EmptySet

