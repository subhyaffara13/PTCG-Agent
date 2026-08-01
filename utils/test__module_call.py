
def test_Module_call():
    T = Poly(cyclotomic_poly(5, x))
    B = PowerBasis(T)
    assert B(0).col.flat() == [1, 0, 0, 0]
    assert B(1).col.flat() == [0, 1, 0, 0]
    col = DomainMatrix.eye(4, ZZ)[:, 2]
    assert B(col).col == col
    raises(ValueError, lambda: B(-1))

