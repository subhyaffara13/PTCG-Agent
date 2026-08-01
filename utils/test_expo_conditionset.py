
def test_expo_conditionset():

    f1 = (exp(x) + 1)**x - 2
    f2 = (x + 2)**y*x - 3
    f3 = 2**x - exp(x) - 3
    f4 = log(x) - exp(x)
    f5 = 2**x + 3**x - 5**x

    assert solveset(f1, x, S.Reals).dummy_eq(ConditionSet(
        x, Eq((exp(x) + 1)**x - 2, 0), S.Reals))
    assert solveset(f2, x, S.Reals).dummy_eq(ConditionSet(
        x, Eq(x*(x + 2)**y - 3, 0), S.Reals))
    assert solveset(f3, x, S.Reals).dummy_eq(ConditionSet(
        x, Eq(2**x - exp(x) - 3, 0), S.Reals))
    assert solveset(f4, x, S.Reals).dummy_eq(ConditionSet(
        x, Eq(-exp(x) + log(x), 0), S.Reals))
    assert solveset(f5, x, S.Reals).dummy_eq(ConditionSet(
        x, Eq(2**x + 3**x - 5**x, 0), S.Reals))

