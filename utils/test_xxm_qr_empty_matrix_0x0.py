
def test_XXM_qr_empty_matrix_0x0(DM):
    T = type(DM([[0]]))
    A = T.zeros((0, 0), QQ)
    Q, R = A.qr()
    assert Q.matmul(R).shape == A.shape
    assert (Q.transpose().matmul(Q)).is_diagonal
    assert R.is_upper
    assert Q.shape == (0, 0)
    assert R.shape == (0, 0)

