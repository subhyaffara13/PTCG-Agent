
def test_DomainMatrix_getitem_sympy():
    dM = DomainMatrix({2: {2: ZZ(2)}, 4: {4: ZZ(1)}}, (5, 5), ZZ)
    val1 = dM.getitem_sympy(0, 0)
    assert val1 is S.Zero
    val2 = dM.getitem_sympy(2, 2)
    assert val2 == 2 and isinstance(val2, Integer)

