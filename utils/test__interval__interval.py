
def test_Interval_Interval():
    assert (SetExpr(Interval(1, 2)) + SetExpr(Interval(10, 20))).set == \
           Interval(11, 22)
    assert (SetExpr(Interval(1, 2))*SetExpr(Interval(10, 20))).set == \
           Interval(10, 40)

