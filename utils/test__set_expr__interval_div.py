
def test_SetExpr_Interval_div():
    # TODO: some expressions cannot be calculated due to bugs (currently
    # commented):
    assert SetExpr(Interval(-3, -2))/SetExpr(Interval(-2, 1)) == SetExpr(Interval(-oo, oo))
    assert SetExpr(Interval(2, 3))/SetExpr(Interval(-2, 2)) == SetExpr(Interval(-oo, oo))

    assert SetExpr(Interval(-3, -2))/SetExpr(Interval(0, 4)) == SetExpr(Interval(-oo, Rational(-1, 2)))
    assert SetExpr(Interval(2, 4))/SetExpr(Interval(-3, 0)) == SetExpr(Interval(-oo, Rational(-2, 3)))
    assert SetExpr(Interval(2, 4))/SetExpr(Interval(0, 3)) == SetExpr(Interval(Rational(2, 3), oo))

    # assert SetExpr(Interval(0, 1))/SetExpr(Interval(0, 1)) == SetExpr(Interval(0, oo))
    # assert SetExpr(Interval(-1, 0))/SetExpr(Interval(0, 1)) == SetExpr(Interval(-oo, 0))
    assert SetExpr(Interval(-1, 2))/SetExpr(Interval(-2, 2)) == SetExpr(Interval(-oo, oo))

    assert 1/SetExpr(Interval(-1, 2)) == SetExpr(Union(Interval(-oo, -1), Interval(S.Half, oo)))

    assert 1/SetExpr(Interval(0, 2)) == SetExpr(Interval(S.Half, oo))
    assert (-1)/SetExpr(Interval(0, 2)) == SetExpr(Interval(-oo, Rational(-1, 2)))
    assert 1/SetExpr(Interval(-oo, 0)) == SetExpr(Interval.open(-oo, 0))
    assert 1/SetExpr(Interval(-1, 0)) == SetExpr(Interval(-oo, -1))

