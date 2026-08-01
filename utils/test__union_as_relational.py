
def test_Union_as_relational():
    x = Symbol('x')
    assert (Interval(0, 1) + FiniteSet(2)).as_relational(x) == \
        Or(And(Le(0, x), Le(x, 1)), Eq(x, 2))
    assert (Interval(0, 1, True, True) + FiniteSet(1)).as_relational(x) == \
        And(Lt(0, x), Le(x, 1))
    assert Or(x < 0, x > 0).as_set().as_relational(x) == \
        And((x > -oo), (x < oo), Ne(x, 0))
    assert (Interval.Ropen(1, 3) + Interval.Lopen(3, 5)
        ).as_relational(x) == And(Ne(x,3),(x>=1),(x<=5))

