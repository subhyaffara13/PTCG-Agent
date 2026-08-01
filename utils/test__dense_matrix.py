
def test_DenseMatrix():
    from aesara.tensor.basic import Join

    t = sy.Symbol('theta')
    for MatrixType in [sy.Matrix, sy.ImmutableMatrix]:
        X = MatrixType([[sy.cos(t), -sy.sin(t)], [sy.sin(t), sy.cos(t)]])
        tX = aesara_code_(X)
        assert isinstance(tX, TensorVariable)
        assert isinstance(tX.owner.op, Join)


def test_DenseMatrix():
    t = sy.Symbol('theta')
    for MatrixType in [sy.Matrix, sy.ImmutableMatrix]:
        X = MatrixType([[sy.cos(t), -sy.sin(t)], [sy.sin(t), sy.cos(t)]])
        tX = theano_code_(X)
        assert isinstance(tX, tt.TensorVariable)
        assert tX.owner.op == tt.join_

