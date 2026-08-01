
def test_issue_10864():
    assert solveset(x**(y*z) - x, x, S.Reals) == FiniteSet(1)

