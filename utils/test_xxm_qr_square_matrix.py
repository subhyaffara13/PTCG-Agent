
def test_XXM_qr_square_matrix(DM):
    lol = [[QQ(3), QQ(1)], [QQ(4), QQ(3)]]
    A = DM(lol)
    Q, R = A.qr()
    assert Q.matmul(R) == A
    assert (Q.transpose().matmul(Q)).is_diagonal
    assert R.is_upper

