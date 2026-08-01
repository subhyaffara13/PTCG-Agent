
def test_issue_9849():
    assert solveset(Abs(sin(x)) + 1, x, S.Reals) == S.EmptySet


def test_issue_9849():
    assert ConditionSet(x, Eq(x, x), S.Naturals
        ) is S.Naturals
    assert ConditionSet(x, Eq(Abs(sin(x)), -1), S.Naturals
        ) == S.EmptySet

