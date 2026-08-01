
def test_issue_11184():
    assert solveset(20*sqrt(y**2 + (sqrt(-(y - 10)*(y + 10)) + 10)**2) - 60, y, S.Reals) is S.EmptySet

