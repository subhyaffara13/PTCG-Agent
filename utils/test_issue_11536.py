
def test_issue_11536():
    assert solveset(0**x - 100, x, S.Reals) == S.EmptySet
    assert solveset(0**x - 1, x, S.Reals) == FiniteSet(0)

