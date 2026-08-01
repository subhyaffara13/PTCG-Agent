
def test_Module_zero():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    assert A.zero().col.flat() == [0, 0, 0, 0]
    assert A.zero().module == A
    assert B.zero().col.flat() == [0, 0, 0, 0]
    assert B.zero().module == B

