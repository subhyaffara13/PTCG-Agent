
def test_Module_basis_elements():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    basis = B.basis_elements()
    bp = B.basis_element_pullbacks()
    for i, (e, p) in enumerate(zip(basis, bp)):
        c = [0] * 4
        assert e.module == B
        assert p.module == A
        c[i] = 1
        assert e == B(to_col(c))
        c[i] = 2
        assert p == A(to_col(c))

