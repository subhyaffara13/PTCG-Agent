
def test_Module_one():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    assert A.one().col.flat() == [1, 0, 0, 0]
    assert A.one().module == A
    assert B.one().col.flat() == [1, 0, 0, 0]
    assert B.one().module == A

