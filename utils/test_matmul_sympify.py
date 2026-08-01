
def test_matmul_sympify():
    assert isinstance(MatMul(eye(1), eye(1)).args[0], Basic)

