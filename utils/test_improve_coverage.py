
def test_improve_coverage():
    solution = solveset(exp(x) + sin(x), x, S.Reals)
    unsolved_object = ConditionSet(x, Eq(exp(x) + sin(x), 0), S.Reals)
    assert solution.dummy_eq(unsolved_object)

