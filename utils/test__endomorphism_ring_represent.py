
def test_EndomorphismRing_represent():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    R = A.endomorphism_ring()
    phi = R.inner_endomorphism(A(1))
    col = R.represent(phi)
    assert col.transpose() == DomainMatrix([
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, -1, -1, -1, -1]
    ], (1, 16), ZZ)

    B = A.submodule_from_matrix(DomainMatrix.zeros((4, 0), ZZ))
    S = B.endomorphism_ring()
    psi = S.inner_endomorphism(A(1))
    col = S.represent(psi)
    assert col == DomainMatrix([], (0, 0), ZZ)

    raises(NotImplementedError, lambda: R.represent(3.14))

