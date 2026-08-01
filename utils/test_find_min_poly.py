
def test_find_min_poly():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    powers = []
    m = find_min_poly(A(1), QQ, x=x, powers=powers)
    assert m == Poly(T, domain=QQ)
    assert len(powers) == 5

    # powers list need not be passed
    m = find_min_poly(A(1), QQ, x=x)
    assert m == Poly(T, domain=QQ)

    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    raises(MissingUnityError, lambda: find_min_poly(B(1), QQ))

