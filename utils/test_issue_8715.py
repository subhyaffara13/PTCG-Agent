
def test_issue_8715():
    eq = x + 1/x > -2 + 1/x
    assert solveset(eq, x, S.Reals) == \
        (Interval.open(-2, oo) - FiniteSet(0))
    assert solveset(eq.subs(x,log(x)), x, S.Reals) == \
        Interval.open(exp(-2), oo) - FiniteSet(1)

