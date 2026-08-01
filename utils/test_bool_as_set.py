
def test_bool_as_set():
    assert ITE(y <= 0, False, y >= 1).as_set() == Interval(1, oo)
    assert And(x <= 2, x >= -2).as_set() == Interval(-2, 2)
    assert Or(x >= 2, x <= -2).as_set() == Interval(-oo, -2) + Interval(2, oo)
    assert Not(x > 2).as_set() == Interval(-oo, 2)
    # issue 10240
    assert Not(And(x > 2, x < 3)).as_set() == \
           Union(Interval(-oo, 2), Interval(3, oo))
    assert true.as_set() == S.UniversalSet
    assert false.as_set() is S.EmptySet
    assert x.as_set() == S.UniversalSet
    assert And(Or(x < 1, x > 3), x < 2).as_set() == Interval.open(-oo, 1)
    assert And(x < 1, sin(x) < 3).as_set() == (x < 1).as_set()
    raises(NotImplementedError, lambda: (sin(x) < 1).as_set())
    # watch for object morph in as_set
    assert Eq(-1, cos(2 * x) ** 2 / sin(2 * x) ** 2).as_set() is S.EmptySet

