
def test_issue_14223():
    assert solveset((Abs(x + Min(x, 2)) - 2).rewrite(Piecewise), x,
        S.Reals) == FiniteSet(-1, 1)
    assert solveset((Abs(x + Min(x, 2)) - 2).rewrite(Piecewise), x,
        Interval(0, 2)) == FiniteSet(1)
    assert solveset(x, x, FiniteSet(1, 2)) is S.EmptySet

