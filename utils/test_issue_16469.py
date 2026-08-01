
def test_issue_16469():
    f = abs(a)
    assert function_range(f, a, S.Reals) == Interval(0, oo, False, True)

