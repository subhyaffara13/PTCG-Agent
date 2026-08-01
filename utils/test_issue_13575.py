
def test_issue_13575():
    assert limit(acos(erfi(x)), x, 1) == acos(erfi(S.One))

