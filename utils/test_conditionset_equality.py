
def test_conditionset_equality():
    ''' Checking equality of different representations of ConditionSet'''
    assert solveset(Eq(tan(x), y), x) == ConditionSet(x, Eq(tan(x), y), S.Complexes)

