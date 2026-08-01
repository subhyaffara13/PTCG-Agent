
def test_Many_Sets():
    assert (SetExpr(Interval(0, 1)) +
            SetExpr(Interval(2, 3)) +
            SetExpr(FiniteSet(10, 11, 12))).set == Interval(12, 16)

