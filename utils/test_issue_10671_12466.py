
def test_issue_10671_12466():
    assert solveset(sin(y), y, Interval(0, pi)) == FiniteSet(0, pi)
    i = Interval(1, 10)
    assert solveset((1/x).diff(x) < 0, x, i) == i
    assert solveset((log(x - 6)/x) <= 0, x, S.Reals) == \
        Interval.Lopen(6, 7)

