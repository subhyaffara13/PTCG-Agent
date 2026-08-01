
def test_issue_9556():
    b = Symbol('b', positive=True)

    assert solveset(Abs(x) + 1, x, S.Reals) is S.EmptySet
    assert solveset(Abs(x) + b, x, S.Reals) is S.EmptySet
    assert solveset(Eq(b, -1), b, S.Reals) is S.EmptySet

