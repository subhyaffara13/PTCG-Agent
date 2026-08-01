
def test_issue_17580():
    assert solveset(1/(1 - x**3)**2, x, S.Reals) is S.EmptySet

