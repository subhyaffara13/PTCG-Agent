
def test_XXM_qr_large_matrix(DM):
    lol = [[QQ(i + j) for j in range(10)] for i in range(10)]
    A = DM(lol)
    Q, R = A.qr()
    assert Q.matmul(R) == A
    assert (Q.transpose().matmul(Q)).is_diagonal
    assert R.is_upper

