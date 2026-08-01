
def test_DomainMatrix_fflu():
    A = DM([[1, 2], [3, 4]], ZZ)
    P, L, D, U = A.fflu()
    assert P.shape == A.shape
    assert L.shape == A.shape
    assert D.shape == A.shape
    assert U.shape == A.shape
    assert P == DM([[1, 0], [0, 1]], ZZ)
    assert L == DM([[1, 0], [3, -2]], ZZ)
    assert D == DM([[1, 0], [0, -2]], ZZ)
    assert U == DM([[1, 2], [0, -2]], ZZ)
    di, d = D.inv_den()
    assert P.matmul(A).rmul(d) == L.matmul(di).matmul(U)

