
def test_isolve_Sets():
    n = Dummy('n')
    assert isolve(Abs(x) <= n, x, relational=False) == \
        Piecewise((S.EmptySet, n < 0), (Interval(-n, n), True))

