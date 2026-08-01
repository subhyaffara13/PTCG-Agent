
def test_interval_symbolic_end_points():
    a = Symbol('a', real=True)

    assert Union(Interval(0, a), Interval(0, 3)).sup == Max(a, 3)
    assert Union(Interval(a, 0), Interval(-3, 0)).inf == Min(-3, a)

    assert Interval(0, a).contains(1) == LessThan(1, a)

