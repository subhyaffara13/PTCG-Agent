
def test_tensor_TensorProduct():
    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)
    assert upretty(TensorProduct(A, B)) == "A\u2297B"
    assert upretty(TensorProduct(A, B, A)) == "A\u2297B\u2297A"

