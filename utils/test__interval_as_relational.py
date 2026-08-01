
def test_Interval_as_relational():
    x = Symbol('x')

    assert Interval(-1, 2, False, False).as_relational(x) == \
        And(Le(-1, x), Le(x, 2))
    assert Interval(-1, 2, True, False).as_relational(x) == \
        And(Lt(-1, x), Le(x, 2))
    assert Interval(-1, 2, False, True).as_relational(x) == \
        And(Le(-1, x), Lt(x, 2))
    assert Interval(-1, 2, True, True).as_relational(x) == \
        And(Lt(-1, x), Lt(x, 2))

    assert Interval(-oo, 2, right_open=False).as_relational(x) == And(Lt(-oo, x), Le(x, 2))
    assert Interval(-oo, 2, right_open=True).as_relational(x) == And(Lt(-oo, x), Lt(x, 2))

    assert Interval(-2, oo, left_open=False).as_relational(x) == And(Le(-2, x), Lt(x, oo))
    assert Interval(-2, oo, left_open=True).as_relational(x) == And(Lt(-2, x), Lt(x, oo))

    assert Interval(-oo, oo).as_relational(x) == And(Lt(-oo, x), Lt(x, oo))
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    assert Interval(x, y).as_relational(x) == (x <= y)
    assert Interval(y, x).as_relational(x) == (y <= x)

