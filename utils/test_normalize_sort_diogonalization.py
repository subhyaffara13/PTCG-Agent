
def test_normalize_sort_diogonalization():
    A = Matrix(((1, 2), (2, 1)))
    P, Q = A.diagonalize(normalize=True)
    assert P*P.T == P.T*P == eye(P.cols)
    P, Q = A.diagonalize(normalize=True, sort=True)
    assert P*P.T == P.T*P == eye(P.cols)
    assert P*Q*P.inv() == A


def test_normalize_sort_diogonalization():
    A = Matrix(((1, 2), (2, 1)))
    P, Q = A.diagonalize(normalize=True)
    assert P*P.T == P.T*P == eye(P.cols)
    P, Q = A.diagonalize(normalize=True, sort=True)
    assert P*P.T == P.T*P == eye(P.cols)
    assert P*Q*P.inv() == A

