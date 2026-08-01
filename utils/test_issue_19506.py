
def test_issue_19506():
    eq = arg(x + I)
    C = Dummy('C')
    assert solveset(eq).dummy_eq(Intersection(ConditionSet(C, Eq(im(C) + 1, 0), S.Complexes),
                                                 ConditionSet(C, re(C) > 0, S.Complexes)))

