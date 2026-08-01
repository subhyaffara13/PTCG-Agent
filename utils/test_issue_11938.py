
def test_issue_11938():
    unit = Interval(0, 1)
    ival = Interval(1, 2)
    cr1 = ComplexRegion(ival * unit)

    assert Intersection(cr1, S.Reals) == ival
    assert Intersection(cr1, unit) == FiniteSet(1)

    arg1 = Interval(0, S.Pi)
    arg2 = FiniteSet(S.Pi)
    arg3 = Interval(S.Pi / 4, 3 * S.Pi / 4)
    cp1 = ComplexRegion(unit * arg1, polar=True)
    cp2 = ComplexRegion(unit * arg2, polar=True)
    cp3 = ComplexRegion(unit * arg3, polar=True)

    assert Intersection(cp1, S.Reals) == Interval(-1, 1)
    assert Intersection(cp2, S.Reals) == Interval(-1, 0)
    assert Intersection(cp3, S.Reals) == FiniteSet(0)

