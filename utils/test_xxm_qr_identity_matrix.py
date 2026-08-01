
def test_XXM_qr_identity_matrix(DM):
    T = type(DM([[0]]))
    A = T.eye(3, QQ)
    Q, R = A.qr()
    assert Q == A
    assert R == A
    assert (Q.transpose().matmul(Q)).is_diagonal
    assert R.is_upper
    assert Q.shape == (3, 3)
    assert R.shape == (3, 3)

