
def test_setexpr():
    se = SetExpr(Interval(0, 1))
    assert isinstance(se.set, Set)
    assert isinstance(se, Expr)

