
def test_issue_10876():
    assert solveset(1/sqrt(x), x) == S.EmptySet

