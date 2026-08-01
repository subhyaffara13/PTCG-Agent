
def test_zero_matmul():
    assert isinstance(S.Zero * MatrixSymbol('X', 2, 2), MatrixExpr)

