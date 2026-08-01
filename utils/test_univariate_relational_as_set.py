
def test_univariate_relational_as_set():
    assert (x > 0).as_set() == Interval(0, oo, True, True)
    assert (x >= 0).as_set() == Interval(0, oo)
    assert (x < 0).as_set() == Interval(-oo, 0, True, True)
    assert (x <= 0).as_set() == Interval(-oo, 0)
    assert Eq(x, 0).as_set() == FiniteSet(0)
    assert Ne(x, 0).as_set() == Interval(-oo, 0, True, True) + \
        Interval(0, oo, True, True)

    assert (x**2 >= 4).as_set() == Interval(-oo, -2) + Interval(2, oo)

