
def test_XXM_qr_linearly_dependent_columns(DM):
    lol = [[QQ(1), QQ(2)], [QQ(2), QQ(4)]]
    A = DM(lol)
    Q, R = A.qr()
    assert Q.matmul(R) == A
    assert (Q.transpose().matmul(Q)).is_diagonal
    assert R.is_upper

