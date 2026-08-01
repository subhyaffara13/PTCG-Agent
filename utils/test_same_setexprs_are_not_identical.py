
def test_same_setexprs_are_not_identical():
    a = SetExpr(FiniteSet(0, 1))
    b = SetExpr(FiniteSet(0, 1))
    assert (a + b).set == FiniteSet(0, 1, 2)

