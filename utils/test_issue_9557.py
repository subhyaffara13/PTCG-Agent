
def test_issue_9557():
    assert solveset(x**2 + a, x, S.Reals) == Intersection(S.Reals,
        FiniteSet(-sqrt(-a), sqrt(-a)))

