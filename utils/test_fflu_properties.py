
def test_fflu_properties():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    P, L, D, U = A.fflu()
    assert P.shape == (2, 2)
    assert L.shape == (2, 2)
    assert D.shape == (2, 2)
    assert U.shape == (2, 2)
    assert L.is_lower
    assert U.is_upper
    assert D.is_diagonal
    di, d = D.inv_den()
    assert P.matmul(A).rmul(d) == L.matmul(di).matmul(U)

