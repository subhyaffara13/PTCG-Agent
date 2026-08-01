
def test_issue_11064():
    eq = x + sqrt(x**2 - 5)
    assert solveset(eq > 0, x, S.Reals) == \
        Interval(sqrt(5), oo)
    assert solveset(eq < 0, x, S.Reals) == \
        Interval(-oo, -sqrt(5))
    assert solveset(eq > sqrt(5), x, S.Reals) == \
        Interval.Lopen(sqrt(5), oo)

