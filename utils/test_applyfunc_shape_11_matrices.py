
def test_applyfunc_shape_11_matrices():
    M = MatrixSymbol("M", 1, 1)

    double = Lambda(x, x*2)

    expr = M.applyfunc(sin)
    assert isinstance(expr, ElementwiseApplyFunction)

    expr = M.applyfunc(double)
    assert isinstance(expr, MatMul)
    assert expr == 2*M

