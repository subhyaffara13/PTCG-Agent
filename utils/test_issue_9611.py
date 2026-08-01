
def test_issue_9611():
    assert solveset(Eq(x - x + a, a), x, S.Reals) == S.Reals
    assert solveset(Eq(y - y + a, a), y) == S.Complexes

