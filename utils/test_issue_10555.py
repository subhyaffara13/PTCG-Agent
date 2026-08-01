
def test_issue_10555():
    f = Function('f')
    g = Function('g')
    assert solveset(f(x) - pi/2, x, S.Reals).dummy_eq(
        ConditionSet(x, Eq(f(x) - pi/2, 0), S.Reals))
    assert solveset(f(g(x)) - pi/2, g(x), S.Reals).dummy_eq(
        ConditionSet(g(x), Eq(f(g(x)) - pi/2, 0), S.Reals))

