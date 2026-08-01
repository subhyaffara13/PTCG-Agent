
def test_XXM_qr_matrix_with_zero_columns(DM):
    lol = [[QQ(3), QQ(0)], [QQ(4), QQ(0)]]
    A = DM(lol)
    Q, R = A.qr()
    assert Q.matmul(R) == A
    assert (Q.transpose().matmul(Q)).is_diagonal
    assert R.is_upper

