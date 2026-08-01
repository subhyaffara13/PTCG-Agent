
def test_SetKind_ConditionSet():
    assert ConditionSet(x, Eq(sin(x), 0), Interval(0, 2*pi)).kind is SetKind(NumberKind)
    assert ConditionSet(x, x < 0).kind is SetKind(NumberKind)

