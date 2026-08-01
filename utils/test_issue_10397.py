
def test_issue_10397():
    assert solveset(sqrt(x), x, S.Complexes) == FiniteSet(0)

