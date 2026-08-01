
def test_Interval_FiniteSet():
    assert (SetExpr(FiniteSet(1, 2)) + SetExpr(Interval(0, 10))).set == \
           Interval(1, 12)

