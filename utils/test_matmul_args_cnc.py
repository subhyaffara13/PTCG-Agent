
def test_matmul_args_cnc():
    assert MatMul(n, A, A.T).args_cnc() == [[n], [A, A.T]]
    assert MatMul(A, A.T).args_cnc() == [[], [A, A.T]]

