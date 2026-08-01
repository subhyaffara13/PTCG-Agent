
def test_FiniteSet_FiniteSet():
    assert (SetExpr(FiniteSet(1, 2, 3)) + SetExpr(FiniteSet(1, 2))).set == \
           FiniteSet(2, 3, 4, 5)
    assert (SetExpr(FiniteSet(1, 2, 3))*SetExpr(FiniteSet(1, 2))).set == \
           FiniteSet(1, 2, 3, 4, 6)

