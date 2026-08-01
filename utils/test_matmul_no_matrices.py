
def test_matmul_no_matrices():
    assert MatMul(1) == 1
    assert MatMul(n, m) == n*m
    assert not isinstance(MatMul(n, m), MatMul)

