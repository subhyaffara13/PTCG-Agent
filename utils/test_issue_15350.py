
def test_issue_15350():
    assert solveset(diff(sqrt(1/x+x))) == FiniteSet(-1, 1)

