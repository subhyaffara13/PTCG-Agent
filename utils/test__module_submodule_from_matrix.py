
def test_Module_submodule_from_matrix():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    e = B(to_col([1, 2, 3, 4]))
    f = e.to_parent()
    assert f.col.flat() == [2, 4, 6, 8]
    # Matrix must be over ZZ:
    raises(ValueError, lambda: A.submodule_from_matrix(DomainMatrix.eye(4, QQ)))
    # Number of rows of matrix must equal number of generators of module A:
    raises(ValueError, lambda: A.submodule_from_matrix(2 * DomainMatrix.eye(5, ZZ)))

